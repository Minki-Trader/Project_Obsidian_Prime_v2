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
from stage_pipelines.stage267 import run267AC_noncalendar_state_guard_score_table_materialization as source_materialization
from stage_pipelines.stage267 import run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review as source_review
from stage_pipelines.stage267 import run267AF_noncalendar_state_guard_followup_or_prune_design as source_design
from stage_pipelines.stage267 import run267AB_noncalendar_weak_slice_resilience_queue as source_state_queue
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267AG"
RUN_ID = "run267AG_stage267_noncalendar_state_guard_followup_queue_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267AG_noncalendar_state_guard_followup_queue_materialized_execution_pending"
JUDGMENT = "followup_queue_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AH_execute_noncalendar_state_guard_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_followup_queue_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_AF_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_AF_DECISION_PATH = source_design.FOLLOWUP_PRUNE_DECISION_PATH
SOURCE_AF_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_AF_REPORT_PATH = source_design.REPORT_PATH
SOURCE_AC_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_AC_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_AB_REPEATED_STATE_PATH = source_state_queue.REPEATED_STATE_SUMMARY_PATH
SOURCE_AB_STATE_CONTRAST_PATH = source_state_queue.WEAK_SLICE_STATE_CONTRAST_PATH
SOURCE_AE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_AE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH

SHARED_STATE_CONTRAST_PATH = RUN_ROOT / "shared_state_contrast.csv"
GUARD_MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "guard_materialization_queue.csv"
FOLLOWUP_VARIANT_MANIFEST_PATH = RUN_ROOT / "followup_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
MODEL_PRESSURE_AUDIT_PATH = RUN_ROOT / "model_pressure_audit.csv"
CONTROL_AUDIT_PATH = RUN_ROOT / "control_audit.csv"
CANDIDATE_ROLE_DECISION_PATH = RUN_ROOT / "candidate_role_decision.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AG_noncalendar_state_guard_followup_queue_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AG_noncalendar_state_guard_followup_queue_materialization.py")

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

COMMON_ROOT = "OPV2/s267ag/run267AG_noncalendar_state_guard_followup"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_MATERIALIZATION_TYPE = "research_score_table_noncalendar_state_guard_followup_pressure_v2"
CSV_MODEL_COLUMNS = source_materialization.CSV_MODEL_COLUMNS
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN

PRESSURE_PROFILES: dict[str, tuple[tuple[float, float, float], ...]] = {
    "aia_dual_replacement_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.040, 0.080, -0.040),
        (-0.080, 0.160, -0.080),
        (-0.120, 0.240, -0.120),
    ),
    "aih_core_role_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.050, 0.100, -0.050),
        (-0.100, 0.200, -0.100),
        (-0.150, 0.300, -0.150),
    ),
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


def split_semicolon(value: Any) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


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


def require_inputs() -> None:
    required = [
        SOURCE_AF_QUEUE_PATH,
        SOURCE_AF_DECISION_PATH,
        SOURCE_AF_FAILURE_MEMORY_PATH,
        SOURCE_AC_VARIANT_MANIFEST_PATH,
        SOURCE_AC_RUNTIME_CONTRACT_PATH,
        SOURCE_AB_REPEATED_STATE_PATH,
        SOURCE_AB_STATE_CONTRAST_PATH,
        SOURCE_AE_CANDIDATE_TEST_REVIEW_PATH,
        SOURCE_AE_NEGATIVE_SLICE_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def variants_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("source_test_id", "")): row
        for row in read_csv(SOURCE_AC_VARIANT_MANIFEST_PATH)
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def contracts_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("source_test_id", "")): row
        for row in read_csv(SOURCE_AC_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def build_shared_state_contrast() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_AB_REPEATED_STATE_PATH):
        focus_count = as_int(row.get("focus_row_count"))
        candidate_count = as_int(row.get("candidate_count"))
        enrichment = as_float(row.get("enrichment_mean"))
        weak_net_sum = as_float(row.get("weak_net_sum"))
        if focus_count >= 5 and candidate_count >= 4 and enrichment >= 1.20:
            read = "shared_state_supported_for_bounded_followup"
        elif focus_count >= 3 and candidate_count >= 3 and enrichment >= 1.15:
            read = "candidate_state_supported_with_boundary"
        else:
            read = "state_watch_only"
        rows.append(
            {
                "state_feature": row.get("state_feature"),
                "state_bucket": row.get("state_bucket"),
                "focus_row_count": focus_count,
                "candidate_count": candidate_count,
                "affected_candidate_aliases": row.get("affected_candidate_aliases"),
                "affected_tests": row.get("affected_tests"),
                "weak_net_sum": weak_net_sum,
                "enrichment_mean": enrichment,
                "materialization_read": row.get("materialization_read"),
                "run267AG_state_read": read,
                "calendar_literal_filter_allowed": "false",
                "decision_effect": "allow_bounded_state_guard_followup" if read != "state_watch_only" else "keep_as_attribution_only",
            }
        )
    return rows


def source_review_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("test_id", "")): row
        for row in read_csv(SOURCE_AE_CANDIDATE_TEST_REVIEW_PATH)
        if row.get("candidate_alias") and row.get("test_id")
    }


def build_guard_materialization_queue(shared_state_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    shared_support = any(row.get("run267AG_state_read") == "shared_state_supported_for_bounded_followup" for row in shared_state_rows)
    review = source_review_by_alias_test()
    queue_rows: list[dict[str, Any]] = [
        {
            "queue_id": "run267AG_q01_shared_state_hole_attribution",
            "priority": "P0",
            "candidate_alias": "all_baseline_candidates",
            "candidate_id": "all_baseline_candidates",
            "candidate_role": "shared_attribution",
            "source_test_id": "all_run267AE_candidate_tests",
            "source_queue_id": "run267AF_q01_shared_state_hole_attribution",
            "followup_profile": "state_contrast_only",
            "source_guard_state_features": "historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;abs_di_spread_14=mid_or_high;atr_14_over_atr_50=high",
            "source_evidence": "run267AB repeated_state_summary plus run267AE negative_slice_summary",
            "materialization_status": "state_contrast_only_no_mt5_attempt",
            "reason": "confirm_noncalendar_state_support_before_more_tuning",
            "success_criteria": "shared_state_rows_support_weak_slices_without_literal_calendar_filter",
            "failure_criteria": "loss_pattern_only_follows_Monday_or_2024_12",
            "stop_condition": "do_not_create_literal_weekday_or_month_filter",
            "claim_boundary": "attribution_only_no_candidate_selection_no_onnx",
        }
    ]
    selected = [
        ("run267AG_q02a_s264_aia_rep_trend_strength_adx_pressure", "P0", "s264_aia", "rep_trend_strength_adx", "aia_dual_replacement_pressure_v2", "bounded_followup_materialization"),
        ("run267AG_q02b_s264_aia_rep_volatility_atr_pressure", "P0", "s264_aia", "rep_volatility_atr", "aia_dual_replacement_pressure_v2", "bounded_followup_materialization"),
        ("run267AG_q04_s264_aih_core_role_pressure", "P2", "s264_aih", "abl_volatility_bandwidth", "aih_core_role_pressure_v2", "one_bounded_pressure_then_downgrade_if_fail"),
    ]
    variants = variants_by_alias_test()
    for queue_id, priority, alias, test_id, profile, reason in selected:
        source = variants.get((alias, test_id))
        review_row = review.get((alias, test_id), {})
        status = "ready_for_score_table_materialization" if source and (alias != "s264_aih" or shared_support) else "blocked_missing_source_or_shared_state_support"
        queue_rows.append(
            {
                "queue_id": queue_id,
                "priority": priority,
                "candidate_alias": alias,
                "candidate_id": source.get("candidate_id", "") if source else "",
                "candidate_role": source.get("candidate_role", "") if source else "",
                "source_test_id": test_id,
                "source_queue_id": source.get("queue_id", "") if source else "",
                "followup_profile": profile,
                "source_guard_state_features": source.get("guard_state_features", "") if source else "",
                "source_evidence": f"net={review_row.get('net_profit','')};pf={review_row.get('profit_factor','')};trades={review_row.get('trade_count','')};worst_month={review_row.get('worst_month','')}:{review_row.get('worst_month_net','')};worst_slice={review_row.get('worst_slice_axis','')}:{review_row.get('worst_slice_bucket','')}:{review_row.get('worst_slice_net','')}",
                "materialization_status": status,
                "reason": reason,
                "success_criteria": "next_MT5_preserves_trade_count_and_reduces_month_or_slice_hole",
                "failure_criteria": "trade_supply_collapses_or_weak_slice_loss_remains_deep",
                "stop_condition": "one_materialization_plus_one_MT5_review_before_prune_or_downgrade",
                "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
            }
        )
    queue_rows.append(
        {
            "queue_id": "run267AG_q03_s264_lc_high_net_control_audit",
            "priority": "P1",
            "candidate_alias": "s264_lc",
            "candidate_id": "s264_lowrank_control",
            "candidate_role": "defensive_control",
            "source_test_id": "abl_gate_variant_rule",
            "source_queue_id": "run267AB_q06_s264_lc_abl_gate_variant_rule",
            "followup_profile": "control_audit_only",
            "source_guard_state_features": "historical_vol_5_over_20=high;abs_di_spread_14=high;atr_14_over_atr_50=high",
            "source_evidence": "high_net_but_2024_12_and_Monday_tail_risk",
            "materialization_status": "audit_only_not_materialized",
            "reason": "do_not_extend_adapter_until_tail_concentration_is_explained",
            "success_criteria": "high_net_explained_without_uncomfortable_tail_risk",
            "failure_criteria": "net_profit_depends_on_unstable_slice_or_hidden_tail_risk",
            "stop_condition": "no_adapter_extension_from_high_net_rank_alone",
            "claim_boundary": "control_audit_only_no_candidate_selection_no_onnx",
        }
    )
    return queue_rows


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


def pressure_terms_text(terms: Sequence[Sequence[float]]) -> str:
    return ";".join("/".join(f"{value:.3f}" for value in row) for row in terms)


def write_pressure_model(source: Path, destination: Path, guard_feature_index: int, profile: str) -> dict[str, Any]:
    terms = PRESSURE_PROFILES[profile]
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
        else:
            non_guard_changed = False or non_guard_changed
        out_rows.append(current)
    if guard_score_rows != len(terms):
        raise RuntimeError(f"guard score row count mismatch for {source}: {guard_score_rows} != {len(terms)}")
    write_runtime_csv(destination, out_rows, CSV_MODEL_COLUMNS)
    return {
        "source_runtime_model_file": rel(source),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "pressure_profile": profile,
        "pressure_terms": pressure_terms_text(terms),
        "guard_score_rows": guard_score_rows,
        "changed_guard_score_rows": changed_rows,
        "non_guard_rows_changed": non_guard_changed,
        "neutral_bins_preserved": neutral_bins_preserved,
    }


def materialize_variant(
    queue_row: Mapping[str, str],
    source_variant: Mapping[str, str],
    source_contract: Mapping[str, str],
    spec: Any,
    index: int,
) -> dict[str, Any]:
    alias = str(queue_row["candidate_alias"])
    test_id = str(queue_row["source_test_id"])
    queue_id = str(queue_row["queue_id"])
    profile = str(queue_row["followup_profile"])
    queue_token = safe_token(queue_id, 72)
    test_token = safe_token(test_id, 48)
    local_root = VARIANT_ROOT / alias / queue_token
    feature_path = local_root / "features" / f"{alias}_{test_token}_followup_guard.csv"
    model_path = local_root / "models" / f"{alias}_{test_token}_followup_guard_model.csv"

    feature_meta = copy_runtime_feature(repo_path(str(source_variant["runtime_feature_file"])), feature_path)
    guard_feature_index = as_int(source_variant.get("guard_score_feature_index"), feature_meta["feature_count"] - 1)
    model_meta = write_pressure_model(repo_path(str(source_variant["runtime_model_file"])), model_path, guard_feature_index, profile)

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    feature_order = list(feature_meta["feature_order"])
    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(test_id, 28)}_followup", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{safe_token(test_id, 28)}_followup", "rt"),
        ),
        start=1,
    ):
        magic = 26731000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_NoncalendarStateGuardFollowup__{safe_token(test_id, 32)}",
            attempt_name=f"{queue_token}_{token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{alias}_{safe_token(test_id, 36)}_followup_guard_v1",
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
                "followup_profile": profile,
                "source_guard_state_features": queue_row.get("source_guard_state_features"),
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
        "followup_profile": profile,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_variant_manifest": rel(SOURCE_AC_VARIANT_MANIFEST_PATH),
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
        "pressure_terms": model_meta["pressure_terms"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": test_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267AC feature order;followup pressure score-table terms;attempt set/ini identity",
        "feature_count": feature_meta["feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
        "long_threshold": as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
        "min_margin": as_float(source_contract.get("min_margin"), 0.0),
        "max_hold_bars": as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
        "followup_profile": profile,
        "known_difference": "uses run267AC runtime feature surface and changes only guard score-table terms; no retraining and no calendar literal filter",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    audit = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": test_id,
        "source_model_file": model_meta["source_runtime_model_file"],
        "runtime_model_file": model_meta["runtime_model_file"],
        "pressure_profile": profile,
        "guard_score_feature_index": guard_feature_index,
        "pressure_terms": model_meta["pressure_terms"],
        "guard_score_rows": model_meta["guard_score_rows"],
        "changed_guard_score_rows": model_meta["changed_guard_score_rows"],
        "non_guard_rows_changed": model_meta["non_guard_rows_changed"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "audit_read": "pass_guard_terms_only" if model_meta["neutral_bins_preserved"] and not model_meta["non_guard_rows_changed"] else "invalid",
    }
    if audit["audit_read"] != "pass_guard_terms_only":
        raise RuntimeError(f"pressure model audit failed for {queue_id}: {audit}")
    return {"variant": variant, "contract": contract, "audit": audit, "attempts": attempts, "feature_path": feature_path, "model_path": model_path}


def build_control_audit() -> list[dict[str, Any]]:
    review = source_review_by_alias_test().get(("s264_lc", "abl_gate_variant_rule"), {})
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_AE_NEGATIVE_SLICE_PATH):
        if row.get("candidate_alias") != "s264_lc" or row.get("test_id") != "abl_gate_variant_rule":
            continue
        rows.append(
            {
                "candidate_alias": "s264_lc",
                "candidate_id": "s264_lowrank_control",
                "test_id": "abl_gate_variant_rule",
                "audit_subject": "high_net_control_tail_risk",
                "overall_net_profit": review.get("net_profit"),
                "overall_profit_factor": review.get("profit_factor"),
                "overall_trade_count": review.get("trade_count"),
                "overall_drawdown_percent": review.get("report_equity_drawdown_percent"),
                "axis": row.get("axis"),
                "bucket": row.get("bucket"),
                "slice_net_profit": row.get("net_profit"),
                "slice_trade_count": row.get("trade_count"),
                "slice_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "slice_read": row.get("slice_read"),
                "audit_judgment": "control_only_tail_risk_unresolved",
                "decision_effect": "do_not_extend_s264_lc_adapter_path_from_high_net_rank",
            }
        )
    return rows


def build_candidate_role_decisions(materialization_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized = {str(row.get("candidate_alias")) for row in materialization_queue if row.get("materialization_status") == "ready_for_score_table_materialization"}
    output: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_AF_DECISION_PATH):
        alias = str(row.get("candidate_alias"))
        if alias == "s264_aia":
            run267ag_decision = "bounded_followup_materialized_watch_not_selection"
        elif alias == "s264_lc":
            run267ag_decision = "control_audit_only_not_adapter_extension"
        elif alias == "s264_aih" and alias in materialized:
            run267ag_decision = "one_pressure_pass_materialized_then_downgrade_if_fail"
        elif alias == "s262_lih":
            run267ag_decision = "hold_as_validation_control_no_new_materialization"
        elif alias == "s258_stc":
            run267ag_decision = "hold_as_stress_boundary_no_new_materialization"
        else:
            run267ag_decision = "no_new_materialization"
        current = dict(row)
        current["run267AG_decision_label"] = run267ag_decision
        current["run267AG_materialized"] = "true" if alias in materialized else "false"
        current["run267AG_claim_boundary"] = "no_selected_candidate_no_onnx_no_goal_achieve"
        output.append(current)
    return output


def build_failure_memory() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(SOURCE_AF_FAILURE_MEMORY_PATH)]
    rows.extend(
        [
            {
                "memory_id": "run267AG_failure_001_s264_lc_high_net_control_not_adapter_leader",
                "pattern": "s264_lc_high_net_still_has_2024_12_and_Monday_tail_concentration",
                "evidence": "run267AE s264_lc net=1620.53;2024_12=-297.93;Monday=-275.09;DD=21.27",
                "affected_scope": "s264_lc",
                "do_not_repeat": "do_not_select_or_extend_s264_lc_adapter_path_from_high_net_rank_alone",
                "salvage_angle": "keep_as_trade_supply_and_gate_shape_control_audit",
                "reopen_condition": "tail_concentration_explained_and_reduced_without_calendar_literal_filter",
                "boundary": "control_audit_not_candidate_selection",
            },
            {
                "memory_id": "run267AG_failure_002_s264_aih_core_role_requires_one_pressure_pass_only",
                "pattern": "s264_aih_core_role_has_no_clean_constructive_run267AE_row",
                "evidence": "constructive_curve_count=0;weakest_slice=Monday:-314.12",
                "affected_scope": "s264_aih",
                "do_not_repeat": "do_not_keep_core_challenger_role_by_old_preference_if_run267AH_fails",
                "salvage_angle": "one_bounded_state_guard_pressure_pass",
                "reopen_condition": "run267AH_creates_clean_curve_without_month_or_deep_slice_hole",
                "boundary": "role_pressure_not_selection",
            },
        ]
    )
    return rows


def build_materialization() -> dict[str, Any]:
    require_inputs()
    shared_state = build_shared_state_contrast()
    materialization_queue = build_guard_materialization_queue(shared_state)
    ready_rows = [row for row in materialization_queue if row.get("materialization_status") == "ready_for_score_table_materialization"]
    source_variants = variants_by_alias_test()
    source_contracts = contracts_by_alias_test()
    specs = specs_by_alias()
    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []
    for index, queue_row in enumerate(ready_rows, start=1):
        key = (str(queue_row["candidate_alias"]), str(queue_row["source_test_id"]))
        source_variant = source_variants.get(key)
        source_contract = source_contracts.get(key)
        if source_variant is None or source_contract is None:
            raise KeyError(f"missing run267AC source variant/contract for {key}")
        item = materialize_variant(queue_row, source_variant, source_contract, specs[str(queue_row["candidate_alias"])], index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        audits.append(item["audit"])
        attempts.extend(item["attempts"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AG_{safe_token(str(queue_row['queue_id']), 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AG runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AG_{safe_token(str(queue_row['queue_id']), 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AG follow-up guard score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )
    control_audit = build_control_audit()
    candidate_role_decisions = build_candidate_role_decisions(materialization_queue)
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
        "shared_state_rows": len(shared_state),
        "guard_queue_rows": len(materialization_queue),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "control_audit_rows": len(control_audit),
        "candidate_role_decision_rows": len(candidate_role_decisions),
        "failure_memory_rows": len(failure_memory),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "reference_scout": "not_required_pure_internal_stage_materialization_reusing_existing_project_helpers",
        "claim_boundary": CLAIM_BOUNDARY,
        "shared_state_contrast": shared_state,
        "guard_materialization_queue": materialization_queue,
        "followup_variant_manifest": variants,
        "runtime_contract": contracts,
        "model_pressure_audit": audits,
        "attempts": attempts,
        "control_audit": control_audit,
        "candidate_role_decisions": candidate_role_decisions,
        "failure_memory": failure_memory,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AF_queue": rel(SOURCE_AF_QUEUE_PATH),
            "run267AF_decisions": rel(SOURCE_AF_DECISION_PATH),
            "run267AF_failure_memory": rel(SOURCE_AF_FAILURE_MEMORY_PATH),
            "run267AC_variant_manifest": rel(SOURCE_AC_VARIANT_MANIFEST_PATH),
            "run267AC_runtime_contract": rel(SOURCE_AC_RUNTIME_CONTRACT_PATH),
            "run267AB_repeated_state_summary": rel(SOURCE_AB_REPEATED_STATE_PATH),
            "run267AB_state_contrast": rel(SOURCE_AB_STATE_CONTRAST_PATH),
            "run267AE_candidate_test_review": rel(SOURCE_AE_CANDIDATE_TEST_REVIEW_PATH),
            "run267AE_negative_slice_summary": rel(SOURCE_AE_NEGATIVE_SLICE_PATH),
        },
        "outputs": {
            "shared_state_contrast": rel(SHARED_STATE_CONTRAST_PATH),
            "guard_materialization_queue": rel(GUARD_MATERIALIZATION_QUEUE_PATH),
            "followup_variant_manifest": rel(FOLLOWUP_VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "model_pressure_audit": rel(MODEL_PRESSURE_AUDIT_PATH),
            "control_audit": rel(CONTROL_AUDIT_PATH),
            "candidate_role_decision": rel(CANDIDATE_ROLE_DECISION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
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
    result["result_judgment"] = build_result_judgment(result)
    return result


def build_experiment_design_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "hypothesis", "value": "run267AE_weak_month_and_weekday_holes_are_noncalendar_state_expressions_that_can_be_pressure_tested_without_literal_calendar_filters"},
        {"field": "decision_use", "value": "create_bounded_followup_MT5_attempt_inputs_and_control_audit_only_no_candidate_selection"},
        {"field": "comparison_baseline", "value": "run267AC state_guard score tables and run267AE curve_time_slice_trade_quality review"},
        {"field": "control_variables", "value": "same_2024_period_same_candidate_pool_same_run267AC_feature_order_same_thresholds_same_EA_runtime_probe"},
        {"field": "changed_variables", "value": "guard_score_table_pressure_terms_only_for_s264_aia_dual_replacement_and_s264_aih_role_pressure"},
        {"field": "sample_scope", "value": "Tier A and Tier A+B 2024 historical runtime attempts planned; Tier A+B remains fallback-disabled duplicate boundary"},
        {"field": "success_criteria", "value": "future_MT5_preserves_trade_count_and_reduces_worst_month_or_worst_slice_without_calendar_literal_filter"},
        {"field": "failure_criteria", "value": "trade_supply_collapses_or_Monday_2024_12_holes_remain_deep_after_one_followup_pass"},
        {"field": "invalid_conditions", "value": "calendar_literal_filter_or_untracked_feature_order_or_claiming_selected_candidate_from_materialization"},
        {"field": "stop_conditions", "value": "do_not_extend_this_followup_branch_after_run267AH_review_if_deep_holes_remain"},
        {"field": "evidence_plan", "value": "shared_state_contrast;guard_materialization_queue;variant_manifest;runtime_contract;attempt_manifest;control_audit;future_MT5_curve_time_slice_review"},
        {"field": "required_gate_coverage", "value": "scope_completion_gate;kpi_contract_audit;skill_receipt_lint;required_gate_coverage_audit"},
    ]


def build_data_integrity_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "data_source", "value": f"{rel(SOURCE_AC_VARIANT_MANIFEST_PATH)} and {rel(SOURCE_AE_CANDIDATE_TEST_REVIEW_PATH)}"},
        {"field": "time_axis", "value": "bar_time_server from run267AC runtime feature files; MT5 test window stays 2024.01.02 through 2025.01.01"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress window; followup variants only for s264_aia dual rows and s264_aih one pressure row"},
        {"field": "missing_or_duplicate_check", "value": f"variant_feature_missing_cells={sum(as_int(row.get('missing_feature_cells')) for row in result['followup_variant_manifest'])};shared_state_rows={result['shared_state_rows']}"},
        {"field": "feature_label_boundary", "value": "no MT5 PnL becomes a label; model is not retrained; only pre-existing guard score feature terms are changed"},
        {"field": "split_boundary", "value": "materialization-only; execution and KPI review remain pending run267AH"},
        {"field": "leakage_risk", "value": "weak-slice evidence influenced followup design, so next run must be read as exploratory pressure not selection proof"},
        {"field": "data_hash_or_identity", "value": f"run_manifest={rel(RUN_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary"},
    ]


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"shared_state_rows={result['shared_state_rows']};variants={result['variant_count']};attempts={result['attempt_count']};control_audit_rows={result['control_audit_rows']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_followup",
            "judgment_label": JUDGMENT,
            "claim_boundary": "materialization_only_no_candidate_selection_no_onnx_no_goal_achieve_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 약한 구간을 달력으로 자르지 않고 시장 상태 압박으로 다시 시험할 입력만 만든 상태다.",
        }
    ]


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
                "source_queue_id": attempt.get("source_queue_id"),
                "followup_profile": attempt.get("followup_profile"),
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
    write_csv(
        SHARED_STATE_CONTRAST_PATH,
        result["shared_state_contrast"],
        (
            "state_feature",
            "state_bucket",
            "focus_row_count",
            "candidate_count",
            "affected_candidate_aliases",
            "affected_tests",
            "weak_net_sum",
            "enrichment_mean",
            "materialization_read",
            "run267AG_state_read",
            "calendar_literal_filter_allowed",
            "decision_effect",
        ),
    )
    write_csv(
        GUARD_MATERIALIZATION_QUEUE_PATH,
        result["guard_materialization_queue"],
        (
            "queue_id",
            "priority",
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "source_test_id",
            "source_queue_id",
            "followup_profile",
            "source_guard_state_features",
            "source_evidence",
            "materialization_status",
            "reason",
            "success_criteria",
            "failure_criteria",
            "stop_condition",
            "claim_boundary",
        ),
    )
    write_csv(
        FOLLOWUP_VARIANT_MANIFEST_PATH,
        result["followup_variant_manifest"],
        (
            "queue_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_queue_id",
            "followup_profile",
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
            "guard_score_feature_index",
            "source_guard_state_features",
            "runtime_rows",
            "signal_rows",
            "missing_feature_cells",
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
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "followup_profile",
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
            "source_queue_id",
            "followup_profile",
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
            "source_model_file",
            "runtime_model_file",
            "pressure_profile",
            "guard_score_feature_index",
            "pressure_terms",
            "guard_score_rows",
            "changed_guard_score_rows",
            "non_guard_rows_changed",
            "neutral_bins_preserved",
            "audit_read",
        ),
    )
    write_csv(
        CONTROL_AUDIT_PATH,
        result["control_audit"],
        (
            "candidate_alias",
            "candidate_id",
            "test_id",
            "audit_subject",
            "overall_net_profit",
            "overall_profit_factor",
            "overall_trade_count",
            "overall_drawdown_percent",
            "axis",
            "bucket",
            "slice_net_profit",
            "slice_trade_count",
            "slice_drawdown_percent",
            "slice_read",
            "audit_judgment",
            "decision_effect",
        ),
    )
    write_csv(
        CANDIDATE_ROLE_DECISION_PATH,
        result["candidate_role_decisions"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "source_test_count",
            "constructive_curve_count",
            "best_test_id",
            "best_net_profit",
            "best_profit_factor",
            "best_trade_count",
            "worst_month_min",
            "worst_drawdown_percent",
            "weakest_slice",
            "risk_flags",
            "run267AF_decision_label",
            "next_use",
            "prune_boundary",
            "reopen_condition",
            "do_not_claim",
            "run267AG_decision_label",
            "run267AG_materialized",
            "run267AG_claim_boundary",
        ),
    )
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], source_design.FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
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
        "shared_state_contrast": rel(SHARED_STATE_CONTRAST_PATH),
        "guard_materialization_queue": rel(GUARD_MATERIALIZATION_QUEUE_PATH),
        "followup_variant_manifest": rel(FOLLOWUP_VARIANT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "attempts": result["attempts"],
        "control_audit": rel(CONTROL_AUDIT_PATH),
        "candidate_role_decision": rel(CANDIDATE_ROLE_DECISION_PATH),
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
        "shared_state_contrast": sha256_file_lf_normalized(SHARED_STATE_CONTRAST_PATH),
        "guard_materialization_queue": sha256_file_lf_normalized(GUARD_MATERIALIZATION_QUEUE_PATH),
        "followup_variant_manifest": sha256_file_lf_normalized(FOLLOWUP_VARIANT_MANIFEST_PATH),
        "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
        "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        "model_pressure_audit": sha256_file_lf_normalized(MODEL_PRESSURE_AUDIT_PATH),
        "control_audit": sha256_file_lf_normalized(CONTROL_AUDIT_PATH),
        "candidate_role_decision": sha256_file_lf_normalized(CANDIDATE_ROLE_DECISION_PATH),
        "failure_memory": sha256_file_lf_normalized(FAILURE_MEMORY_PATH),
        "experiment_design_receipt": sha256_file_lf_normalized(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": sha256_file_lf_normalized(DATA_INTEGRITY_RECEIPT_PATH),
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
        "# Stage267 Run267AG Noncalendar State Guard Follow-up Queue Materialization(267단계 267AG 비달력 상태 방어 후속 큐 물질화)",
        "",
        "- action(행동): run267AF(267AF 실행)의 follow-up/prune queue(후속/가지치기 대기열)를 run267AH(267AH 실행)에서 돌릴 수 있는 materialized inputs(물질화 입력)로 바꿨다.",
        "- effect(효과): s264_aia는 두 replacement(대체) 행을 다시 압박하고, s264_aih는 core role(핵심 역할)을 한 번 더 검증하며, s264_lc는 고순익 control audit(방어 기준 감사)로만 남긴다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AE(267AE 실행)에서 좋은 숫자가 있어도 Monday(월요일)와 2024-12(2024년 12월) 구멍이 계속 남았다. run267AG(267AG 실행)는 그 구멍을 달력 필터(calendar filter, 달력 필터)로 막지 않고, 이미 만든 noncalendar state guard(비달력 상태 방어)를 조금 더 강하게 압박하는 입력을 만들었다.",
        "Effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 진짜로 약한 구간이 줄어드는지 보게 된다. 아직 성과를 확인한 것이 아니라, 확인할 준비를 한 것이다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- shared_state_rows(공통 상태 행): `{result['shared_state_rows']}`",
        f"- guard_queue_rows(방어 큐 행): `{result['guard_queue_rows']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts queued(대기 시도): `{result['attempt_count']}`",
        f"- control_audit_rows(방어 기준 감사 행): `{result['control_audit_rows']}`",
        f"- candidate_role_decisions(후보 역할 결정): `{result['candidate_role_decision_rows']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_rows']}`",
        "",
        "## Candidate Meaning(후보 의미)",
        "",
        "- `s264_aia`: P0 watch(최우선 관찰)로 두 replacement(대체) 행을 다시 압박한다. 선택 후보는 아니다.",
        "- `s264_lc`: 순수익은 높지만 2024-12(2024년 12월)와 Monday(월요일) 꼬리 위험이 있어 control audit(방어 기준 감사)로만 둔다.",
        "- `s264_aih`: core challenger(핵심 도전자) 역할을 한 번 더 압박한다. 다음에도 깨지면 downgrade(강등) 경계다.",
        "- `s262_lih`, `s258_stc`: 이번 run267AG(267AG 실행)에서는 새 물질화 없이 비교/압박 경계로만 보존한다.",
        "",
        "## Boundary(경계)",
        "",
        "- MT5 execution(MT5 실행): `not_executed`",
        "- balance/equity curve(잔액/평가금 곡선): `pending_run267AH`",
        "- trade quality(거래 품질): `pending_run267AH`",
        "- candidate selection(후보 선택): `none`",
        "- ONNX(온닉스): `not_reviewed`",
        "",
        "## Outputs(산출물)",
        "",
        f"- shared_state_contrast(공통 상태 대비): `{rel(SHARED_STATE_CONTRAST_PATH)}`",
        f"- guard_materialization_queue(방어 물질화 큐): `{rel(GUARD_MATERIALIZATION_QUEUE_PATH)}`",
        f"- followup_variant_manifest(후속 변형 목록): `{rel(FOLLOWUP_VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        f"- control_audit(방어 기준 감사): `{rel(CONTROL_AUDIT_PATH)}`",
        f"- candidate_role_decision(후보 역할 결정): `{rel(CANDIDATE_ROLE_DECISION_PATH)}`",
        f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- effect(효과): 6개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해서 거래 목록, 곡선, 시간 구간, 거래 품질을 다시 확인한다.",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267AG_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267AG noncalendar state guard follow-up inputs."),
        ("stage267_run267AG_shared_state_contrast", "state_contrast", SHARED_STATE_CONTRAST_PATH, "Run267AG shared noncalendar state contrast."),
        ("stage267_run267AG_guard_materialization_queue", "materialization_queue", GUARD_MATERIALIZATION_QUEUE_PATH, "Run267AG guard materialization queue."),
        ("stage267_run267AG_followup_variant_manifest", "variant_manifest", FOLLOWUP_VARIANT_MANIFEST_PATH, "Run267AG follow-up variant manifest."),
        ("stage267_run267AG_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267AG runtime contract."),
        ("stage267_run267AG_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267AG MT5 attempt manifest."),
        ("stage267_run267AG_model_pressure_audit", "model_pressure_audit", MODEL_PRESSURE_AUDIT_PATH, "Run267AG model pressure audit."),
        ("stage267_run267AG_control_audit", "control_audit", CONTROL_AUDIT_PATH, "Run267AG s264_lc control audit."),
        ("stage267_run267AG_candidate_role_decision", "candidate_role_decision", CANDIDATE_ROLE_DECISION_PATH, "Run267AG candidate role decision."),
        ("stage267_run267AG_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AG failure memory."),
        ("stage267_run267AG_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AG experiment design receipt."),
        ("stage267_run267AG_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267AG data integrity receipt."),
        ("stage267_run267AG_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AG result judgment."),
        ("stage267_run267AG_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AG run manifest."),
        ("stage267_run267AG_lineage", "lineage", LINEAGE_PATH, "Run267AG lineage."),
        ("stage267_run267AG_review_result", "review_result_json", REVIEW_RESULT_PATH, "Run267AG review result JSON."),
        ("stage267_run267AG_report", "review_report", REPORT_PATH, "Run267AG review report."),
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
        "lane": "noncalendar_state_guard_followup_queue_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"shared_state_rows={result['shared_state_rows']};guard_queue_rows={result['guard_queue_rows']};"
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_followup_queue_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "noncalendar_state_guard_followup_queue_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "noncalendar_state_guard_followup_queue_materialization",
        "tier_scope": "Tier A and Tier A+B 2024 historical runtime attempts planned",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};control_audit_rows={result['control_audit_rows']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267AG_noncalendar_state_guard_followup_queue_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "noncalendar_state_guard_followup_queue_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 followup attempts planned",
        "scoreboard": "feature_model_set_ini_manifest_and_control_audit",
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
    report_line = f"- run267AG_noncalendar_state_guard_followup_queue_materialization(267AG 비달력 상태 방어 후속 큐 물질화): `{rel(REPORT_PATH)}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_followup_queue_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267AF_noncalendar_state_guard_followup_or_prune_design", report_line)
    current = current.replace(
        "- next_run(다음 실행): `run267AG_materialize_noncalendar_state_guard_followup_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- action(행동): run267AF(267AF 실행)는 run267AE(267AE 실행)의 거래/곡선/시간구간 근거를 후보별 후속/가지치기 설계로 바꿨다.",
        "- action(행동): run267AG(267AG 실행)는 run267AF(267AF 실행)의 후속/가지치기 큐를 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 물질화했다.",
    )
    current = current.replace(
        "- effect(효과): 다음 run267AG(267AG 실행)에서 어떤 축을 물질화하고 어떤 후보를 멈출지 큐와 중단 조건을 남겼다.",
        "- effect(효과): 다음 run267AH(267AH 실행)에서 6개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 거래/곡선/시간구간/거래 품질을 확인할 수 있다.",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267AG_materialize_noncalendar_state_guard_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    current = append_block_once(
        current,
        "Run267AG(267AG 실행)는 run267AF",
        "\n".join(
            [
                "Run267AG(267AG 실행)는 run267AF(267AF 실행)의 noncalendar state guard follow-up queue(비달력 상태 방어 후속 큐)를 물질화했다.",
                "Effect(효과): s264_aia 2개 replacement(대체) 압박, s264_aih 1개 role pressure(역할 압박), s264_lc control audit(방어 기준 감사)을 분리했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
            ]
        ),
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267AF_noncalendar_state_guard_followup_or_prune_design", report_line)
    selection = selection.replace(
        "- next_action(다음 행동): `run267AG_materialize_noncalendar_state_guard_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection = append_block_once(
        selection,
        "Run267AG(267AG 실행)는 noncalendar state guard follow-up queue",
        "\n".join(
            [
                "Run267AG(267AG 실행)는 noncalendar state guard follow-up queue(비달력 상태 방어 후속 큐)를 materialized execution pending(물질화 완료, 실행 대기) 상태로 만들었다.",
                "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 없고, run267AH(267AH 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 실제 거래/곡선/시간구간 영향을 확인한다.",
            ]
        ),
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267AF_noncalendar_state_guard_followup_or_prune_design", report_line)
    review = review.replace(
        "- next_action(다음 행동): `run267AG_materialize_noncalendar_state_guard_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    review = append_block_once(
        review,
        "Run267AG(267AG 실행)는 noncalendar state guard follow-up queue",
        "\n".join(
            [
                "Run267AG(267AG 실행)는 noncalendar state guard follow-up queue materialization(비달력 상태 방어 후속 큐 물질화)을 완료했다.",
                "Effect(효과): 3개 follow-up variant(후속 변형)와 6개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었지만, 아직 실행 결과가 아니므로 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267AG(267AG 실행) noncalendar state guard follow-up queue materialization(비달력 상태 방어 후속 큐 물질화) `{STATUS}`. "
        "Effect(효과): run267AF(267AF 실행)의 후속/가지치기 설계를 3개 variant(변형)와 6개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_design.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_design.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267AF_noncalendar_state_guard_followup_or_prune_design_report_path",
        f"  run267AG_noncalendar_state_guard_followup_queue_materialization_report_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace(
        "next_action: run267AG_materialize_noncalendar_state_guard_followup_queue",
        f"next_action: {NEXT_ACTION}",
    )
    workspace = workspace.replace(
        "active_run267AC_noncalendar_state_guard_score_table_materialization(267AC 비달력 상태 방어 점수표 물질화 활성)",
        "active_run267AG_noncalendar_state_guard_followup_queue_materialization(267AG 비달력 상태 방어 후속 큐 물질화 활성)",
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
                "shared_state_rows": final_result["shared_state_rows"],
                "guard_queue_rows": final_result["guard_queue_rows"],
                "variant_count": final_result["variant_count"],
                "attempt_count": final_result["attempt_count"],
                "control_audit_rows": final_result["control_audit_rows"],
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
