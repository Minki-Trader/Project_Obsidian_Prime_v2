from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design as source_design


STAGE_ID = input_probe.STAGE_ID
SOURCE_RUN_ID = source_design.RUN_ID
RUN_NUMBER = "run267Q"
RUN_ID = "run267Q_stage267_internal_feature_order_confirmed_adapter_materialization_v1"
STATUS = "run267Q_internal_feature_order_confirmed_adapter_materialized_execution_pending"
NEXT_ACTION = "run267Q_execute_internal_feature_order_confirmed_adapter_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
MATERIALIZATION_ROOT = RUN_ROOT / "internal_feature_order_confirmed_adapter_materialization"

INPUT_QUEUE_PATH = source_design.ADAPTER_DESIGN_QUEUE_PATH
INPUT_AUDIT_PATH = source_design.INTERNAL_FEATURE_ORDER_AUDIT_PATH
INPUT_DECISION_PATH = source_design.CANDIDATE_AXIS_DECISION_PATH
INPUT_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
INPUT_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH

VARIANT_MANIFEST_PATH = MATERIALIZATION_ROOT / "internal_adapter_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = MATERIALIZATION_ROOT / "runtime_contract.csv"
FEATURE_DIAGNOSTICS_PATH = MATERIALIZATION_ROOT / "feature_diagnostics.csv"
MODEL_AUDIT_PATH = MATERIALIZATION_ROOT / "model_score_table_audit.csv"
ATTEMPT_MANIFEST_PATH = MATERIALIZATION_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = MATERIALIZATION_ROOT / "run_manifest.json"
LINEAGE_PATH = MATERIALIZATION_ROOT / "lineage.json"
RESULT_PATH = MATERIALIZATION_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267Q_internal_feature_order_confirmed_adapter_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267q/run267Q_internal_feature_order_adapter"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")


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
    if path.is_absolute():
        return path
    return REPO_ROOT / path


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
    if isinstance(value, (list, tuple)):
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
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_existing_line_prefix(text: str, prefix: str, replacement: str) -> str:
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
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def index_rows(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row.get(key, "")): dict(row) for row in rows}


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def internal_feature_name(test_id: str) -> str:
    if test_id == "abl_volatility_bandwidth":
        return "stage267q_internal_volatility_bandwidth_adapter_score"
    if test_id == "rep_volatility_atr":
        return "stage267q_internal_volatility_atr_adapter_score"
    return f"stage267q_internal_{safe_token(test_id, 36)}_adapter_score"


def q(values: Sequence[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * float(quantile)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[int(pos)]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def source_added_feature(audit_row: Mapping[str, Any]) -> str:
    feature = str(audit_row.get("added_feature", "")).strip()
    if not feature:
        raise ValueError(f"missing added_feature for {audit_row.get('queue_id')}")
    return feature


def write_internal_feature_file(
    source_feature_path: Path,
    destination: Path,
    source_feature: str,
    target_feature: str,
) -> dict[str, Any]:
    rows = read_csv(source_feature_path)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source_feature_path}")
    base_columns = list(rows[0].keys())
    if source_feature not in base_columns:
        raise KeyError(f"{source_feature} missing in {source_feature_path}")
    if base_columns[0] != "bar_time_server":
        raise ValueError(f"unexpected first feature column: {base_columns[0]}")
    columns = [target_feature if column == source_feature else column for column in base_columns]
    feature_order = list(columns[1:])
    transformed: list[dict[str, Any]] = []
    values: list[float] = []
    mismatches = 0
    changed_rows = 0
    for row in rows:
        source_value = row.get(source_feature, "")
        current: dict[str, Any] = {}
        for column in base_columns:
            out_column = target_feature if column == source_feature else column
            current[out_column] = row.get(column, "")
        value = as_float(source_value)
        values.append(value)
        if str(current.get(target_feature, "")) != str(source_value):
            mismatches += 1
        if value > 0.0:
            changed_rows += 1
        transformed.append(current)
    write_runtime_csv(destination, transformed, columns)
    return {
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "rows": len(transformed),
        "source_feature": source_feature,
        "target_feature": target_feature,
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "score_min": min(values) if values else 0.0,
        "score_q50": q(values, 0.50),
        "score_q80": q(values, 0.80),
        "score_q95": q(values, 0.95),
        "score_max": max(values) if values else 0.0,
        "changed_rows": changed_rows,
        "rename_mismatch_rows": mismatches,
    }


def copy_model(source_model_path: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source_model_path):
        raise FileNotFoundError(source_model_path)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source_model_path), io_path(destination))
    return {
        "source_model_file": rel(source_model_path),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def model_audit(queue_id: str, model_path: Path, feature_count: int, adapter_feature_index: int) -> dict[str, Any]:
    rows = read_csv(model_path)
    if not rows:
        raise RuntimeError(f"empty model file: {model_path}")
    record_counts = Counter(str(row.get("record_type", "")) for row in rows)
    feature_indices = [as_int(row.get("feature_index"), -1) for row in rows if str(row.get("feature_index", "")).strip()]
    max_index = max(feature_indices) if feature_indices else -1
    adapter_rows = [row for row in rows if as_int(row.get("feature_index"), -1) == adapter_feature_index]
    adapter_counts = Counter(str(row.get("record_type", "")) for row in adapter_rows)
    return {
        "queue_id": queue_id,
        "model_file": rel(model_path),
        "model_sha256": sha256_file_lf_normalized(model_path),
        "model_row_count": len(rows),
        "cut_rows": record_counts.get("cut", 0),
        "score_rows": record_counts.get("score", 0),
        "max_feature_index": max_index,
        "feature_count": feature_count,
        "adapter_feature_index": adapter_feature_index,
        "adapter_cut_rows": adapter_counts.get("cut", 0),
        "adapter_score_rows": adapter_counts.get("score", 0),
        "index_policy_status": "matched" if max_index == feature_count - 1 and adapter_feature_index == feature_count - 1 else "mismatch",
    }


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "priority": attempt.get("priority"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def materialize_payload() -> dict[str, Any]:
    queue_rows = [row for row in read_csv(INPUT_QUEUE_PATH) if str(row.get("priority", "")) == "P0"]
    if not queue_rows:
        raise RuntimeError(f"no P0 rows in {INPUT_QUEUE_PATH}")
    audit_by_queue = index_rows(read_csv(INPUT_AUDIT_PATH), "queue_id")
    specs = specs_by_alias()
    created_at = utc_now()
    variant_rows: list[dict[str, Any]] = []
    diagnostics_rows: list[dict[str, Any]] = []
    model_audit_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []

    for variant_index, queue_row in enumerate(sorted(queue_rows, key=lambda row: as_int(row.get("queue_order"))), start=1):
        source_queue_id = str(queue_row["source_queue_id"])
        audit = audit_by_queue.get(source_queue_id)
        if not audit:
            raise KeyError(f"missing audit row for {source_queue_id}")
        alias = str(queue_row["candidate_alias"])
        spec = specs[alias]
        test_id = str(queue_row["test_id"])
        source_feature = source_added_feature(audit)
        target_feature = internal_feature_name(test_id)
        queue_id = f"run267Q_{variant_index:02d}_{alias}_{safe_token(test_id, 36)}"
        queue_token = safe_token(queue_id, 72)
        local_root = MATERIALIZATION_ROOT / "variants" / alias / queue_token
        feature_path = local_root / "features" / f"{alias}_{safe_token(test_id, 48)}_internal_adapter.csv"
        model_path = local_root / "models" / f"{alias}_{safe_token(test_id, 48)}_internal_adapter_model.csv"

        feature_meta = write_internal_feature_file(
            repo_path(str(audit["feature_file"])),
            feature_path,
            source_feature,
            target_feature,
        )
        model_meta = copy_model(repo_path(str(audit["model_file"])), model_path)
        adapter_feature_index = int(feature_meta["feature_count"]) - 1
        model_check = model_audit(queue_id, model_path, int(feature_meta["feature_count"]), adapter_feature_index)
        model_audit_rows.append(model_check)

        common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
        common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
        common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
        common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

        variant_row = {
            "queue_id": queue_id,
            "source_queue_id": source_queue_id,
            "source_run_id": SOURCE_RUN_ID,
            "candidate_id": queue_row["candidate_id"],
            "candidate_alias": alias,
            "candidate_role": queue_row["candidate_role"],
            "priority": queue_row["priority"],
            "test_id": test_id,
            "feature_family": queue_row["feature_family"],
            "source_materialization_boundary": audit["materialization_boundary"],
            "materialization_boundary": "explicit_internal_adapter_feature_materialization_from_proxy_score_v1(대체 점수에서 명시 내부 어댑터 피처 물질화)",
            "model_materialization_type": "copied_ebm_table_with_internal_feature_order_rename_v1",
            "source_feature_file": audit["feature_file"],
            "source_feature_sha256": sha256_file_lf_normalized(repo_path(str(audit["feature_file"]))),
            "feature_file": feature_meta["feature_file"],
            "feature_sha256": feature_meta["feature_sha256"],
            "source_model_file": model_meta["source_model_file"],
            "model_file": model_meta["model_file"],
            "model_sha256": model_meta["model_sha256"],
            "common_feature_path": common_feature_path,
            "common_feature_sha256": common_feature["sha256"],
            "common_model_path": common_model_path,
            "common_model_sha256": common_model["sha256"],
            "source_added_feature": source_feature,
            "internal_adapter_feature": target_feature,
            "feature_count": feature_meta["feature_count"],
            "feature_order": feature_meta["feature_order"],
            "feature_order_hash": feature_meta["feature_order_hash"],
            "source_feature_order_hash": audit["feature_order_hash"],
            "adapter_feature_index": adapter_feature_index,
            "rows": feature_meta["rows"],
            "changed_rows": feature_meta["changed_rows"],
            "rename_mismatch_rows": feature_meta["rename_mismatch_rows"],
            "model_index_policy_status": model_check["index_policy_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        variant_rows.append(variant_row)
        diagnostics_rows.append(
            {
                "queue_id": queue_id,
                "source_queue_id": source_queue_id,
                "candidate_alias": alias,
                "test_id": test_id,
                "source_feature": source_feature,
                "internal_adapter_feature": target_feature,
                "source_feature_order_hash": audit["feature_order_hash"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "feature_count": feature_meta["feature_count"],
                "rows": feature_meta["rows"],
                "changed_rows": feature_meta["changed_rows"],
                "score_min": feature_meta["score_min"],
                "score_q50": feature_meta["score_q50"],
                "score_q80": feature_meta["score_q80"],
                "score_q95": feature_meta["score_q95"],
                "score_max": feature_meta["score_max"],
                "rename_mismatch_rows": feature_meta["rename_mismatch_rows"],
                "feature_order": feature_meta["feature_order"],
            }
        )
        contract_rows.append(
            {
                "queue_id": queue_id,
                "source_queue_id": source_queue_id,
                "candidate_id": queue_row["candidate_id"],
                "candidate_alias": alias,
                "test_id": test_id,
                "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;score_table_csv;internal_adapter_feature_order;attempt set/ini identity",
                "feature_count": feature_meta["feature_count"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "model_backend": "ebm_table",
                "model_materialization_type": "copied_ebm_table_with_internal_feature_order_rename_v1",
                "materialization_boundary": variant_row["materialization_boundary"],
                "short_threshold": spec.variant.short_threshold,
                "long_threshold": spec.variant.long_threshold,
                "min_margin": 0.0,
                "max_hold_bars": spec.variant.max_hold_bars,
                "close_on_flat_signal": spec.variant.close_on_flat_signal,
                "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                "known_difference": "source proxy score is renamed and frozen as explicit internal adapter feature; no MT5 execution yet; not true raw feature ablation",
                "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
            }
        )
        lineage_rows.extend(
            [
                {
                    "queue_id": queue_id,
                    "artifact_role": "feature_csv",
                    "source_path": audit["feature_file"],
                    "run267q_path": feature_meta["feature_file"],
                    "common_path": common_feature_path,
                    "run267q_sha256": feature_meta["feature_sha256"],
                    "common_sha256": common_feature["sha256"],
                },
                {
                    "queue_id": queue_id,
                    "artifact_role": "model_csv",
                    "source_path": model_meta["source_model_file"],
                    "run267q_path": model_meta["model_file"],
                    "common_path": common_model_path,
                    "run267q_sha256": model_meta["model_sha256"],
                    "common_sha256": common_model["sha256"],
                },
            ]
        )

        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(test_id, 26)}_internal", "ta"),
                (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{safe_token(test_id, 26)}_internal", "rt"),
            ),
            start=1,
        ):
            magic = 26710000 + variant_index * 100 + role_index
            payload = attempt_payload(
                run_root=MATERIALIZATION_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label=f"stage267_InternalAdapter__{safe_token(test_id, 32)}",
                attempt_name=f"{queue_token}_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{alias}_{safe_token(test_id, 36)}",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=int(feature_meta["feature_count"]),
                feature_order_hash=str(feature_meta["feature_order_hash"]),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date="2024.01.02",
                to_date="2025.01.01",
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/{alias}/{queue_token}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=input_probe.base_extra_set_values(spec, magic),
            )
            payload.update(
                {
                    "queue_id": queue_id,
                    "source_queue_id": source_queue_id,
                    "candidate_id": queue_row["candidate_id"],
                    "candidate_alias": alias,
                    "candidate_role": queue_row["candidate_role"],
                    "test_id": test_id,
                    "priority": queue_row["priority"],
                    "materialization_boundary": variant_row["materialization_boundary"],
                    "execution_status": "not_executed",
                }
            )
            attempts.append(payload)

    return {
        "created_at_utc": created_at,
        "input_queue": rel(INPUT_QUEUE_PATH),
        "input_audit": rel(INPUT_AUDIT_PATH),
        "variant_manifest": variant_rows,
        "runtime_contract": contract_rows,
        "feature_diagnostics": diagnostics_rows,
        "model_score_table_audit": model_audit_rows,
        "lineage": lineage_rows,
        "attempts": attempts,
    }


def write_outputs(payload: Mapping[str, Any]) -> dict[str, Any]:
    variant_rows = list(payload["variant_manifest"])
    contract_rows = list(payload["runtime_contract"])
    diagnostics_rows = list(payload["feature_diagnostics"])
    model_audit_rows = list(payload["model_score_table_audit"])
    attempts = list(payload["attempts"])
    lineage_rows = list(payload["lineage"])
    write_csv(
        VARIANT_MANIFEST_PATH,
        variant_rows,
        (
            "queue_id",
            "source_queue_id",
            "source_run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "priority",
            "test_id",
            "feature_family",
            "source_materialization_boundary",
            "materialization_boundary",
            "model_materialization_type",
            "source_feature_file",
            "source_feature_sha256",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "source_added_feature",
            "internal_adapter_feature",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "source_feature_order_hash",
            "adapter_feature_index",
            "rows",
            "changed_rows",
            "rename_mismatch_rows",
            "model_index_policy_status",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "queue_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "materialization_boundary",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        FEATURE_DIAGNOSTICS_PATH,
        diagnostics_rows,
        (
            "queue_id",
            "source_queue_id",
            "candidate_alias",
            "test_id",
            "source_feature",
            "internal_adapter_feature",
            "source_feature_order_hash",
            "feature_order_hash",
            "feature_count",
            "rows",
            "changed_rows",
            "score_min",
            "score_q50",
            "score_q80",
            "score_q95",
            "score_max",
            "rename_mismatch_rows",
            "feature_order",
        ),
    )
    write_csv(
        MODEL_AUDIT_PATH,
        model_audit_rows,
        (
            "queue_id",
            "model_file",
            "model_sha256",
            "model_row_count",
            "cut_rows",
            "score_rows",
            "max_feature_index",
            "feature_count",
            "adapter_feature_index",
            "adapter_cut_rows",
            "adapter_score_rows",
            "index_policy_status",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(attempts),
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "priority",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    run_manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": payload["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "source_run_id": SOURCE_RUN_ID,
        "input_queue": rel(INPUT_QUEUE_PATH),
        "input_audit": rel(INPUT_AUDIT_PATH),
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "feature_diagnostics": rel(FEATURE_DIAGNOSTICS_PATH),
            "model_score_table_audit": rel(MODEL_AUDIT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {
            "variant_manifest": sha256_file_lf_normalized(VARIANT_MANIFEST_PATH),
            "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
            "feature_diagnostics": sha256_file_lf_normalized(FEATURE_DIAGNOSTICS_PATH),
            "model_score_table_audit": sha256_file_lf_normalized(MODEL_AUDIT_PATH),
            "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        },
        "variant_count": len(variant_rows),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    write_json(
        LINEAGE_PATH,
        {
            "source_inputs": [
                rel(INPUT_QUEUE_PATH),
                rel(INPUT_AUDIT_PATH),
                rel(INPUT_DECISION_PATH),
                rel(INPUT_FAILURE_MEMORY_PATH),
                rel(INPUT_REVIEW_RESULT_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": run_manifest["outputs"],
            "lineage_rows": lineage_rows,
            "registry_links": ["artifact_registry.csv", "run_registry.csv", "alpha_run_ledger.csv", "stage_run_ledger.csv"],
            "availability": "tracked_plus_common_files_copy(추적 산출물과 Common Files 복사)",
            "lineage_judgment": "connected_with_boundary_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    final_result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "variant_manifest": variant_rows,
        "runtime_contract": contract_rows,
        "feature_diagnostics": diagnostics_rows,
        "model_score_table_audit": model_audit_rows,
        "attempts": attempt_rows(attempts),
        "run_manifest": run_manifest,
        "variant_count": len(variant_rows),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    write_json(RESULT_PATH, final_result)
    write_md(REPORT_PATH, report_markdown(final_result))
    return final_result


def report_markdown(result: Mapping[str, Any]) -> str:
    variants = list(result["variant_manifest"])
    attempts = list(result["attempts"])
    feature_checks = list(result["feature_diagnostics"])
    model_checks = list(result["model_score_table_audit"])
    candidate_counts = Counter(str(row["candidate_alias"]) for row in variants)
    lines = [
        "# Stage267 Run267Q Internal Feature Order Confirmed Adapter Materialization(267Q 내부 피처 순서 확인 어댑터 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- action(행동): run267P(267P 실행)의 P0 Adapter design queue(P0 어댑터 설계 큐) 4개를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.",
        "- effect(효과): volatility/ATR(변동성/ATR) proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처) 이름과 feature order hash(피처 순서 해시)로 고정해 다음 MT5(MetaTrader 5, 메타트레이더5) 실행 입력을 재현 가능하게 했다.",
        f"- variant_count(변형 수): `{len(variants)}`",
        f"- attempt_count(시도 수): `{len(attempts)}`",
        f"- selected_candidate(선택 후보): `{result['selected_candidate']}`",
        f"- ONNX readiness(ONNX 준비): `{result['onnx_readiness']}`",
        f"- Goal Achieve(목표 달성): `{result['goal_achieve']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267Q(267Q 실행)는 아직 성능 검토가 아니다. 이번에는 다음 테스트에 넣을 재료를 정확한 파일로 만든 단계다.",
        "좋아 보였던 volatility/ATR(변동성/ATR) 단서를 내부 Adapter(어댑터) 피처 이름으로 다시 고정했지만, 이것만으로 후보 선택이나 ONNX(ONNX) 검토로 가지 않는다.",
        "다음에는 이 산출물을 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌려 곡선, 약한 구간, 거래 품질이 유지되는지 확인해야 한다.",
        "",
        "## Materialized Variants(물질화 변형)",
        "",
        "| candidate(후보) | test(시험) | feature(피처) | rows(행) | feature hash(피처 해시) |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in variants:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['internal_adapter_feature']}` | {row['rows']} | `{row['feature_order_hash']}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Coverage(후보별 포함)",
            "",
            "| candidate(후보) | variants(변형) |",
            "| --- | ---: |",
        ]
    )
    for candidate, count in sorted(candidate_counts.items()):
        lines.append(f"| `{candidate}` | {count} |")
    lines.extend(
        [
            "",
            "## Checks(점검)",
            "",
            f"- feature_rename_mismatch_rows(피처 이름 변경 불일치 행): `{sum(int(row['rename_mismatch_rows']) for row in feature_checks)}`",
            f"- model_index_policy_mismatch(모델 인덱스 정책 불일치): `{sum(1 for row in model_checks if row['index_policy_status'] != 'matched')}`",
            f"- attempts_pending_execution(실행 대기 시도): `{len(attempts)}`",
            "- runtime_claim_boundary(런타임 주장 경계): `research_only_execution_pending_no_selected_candidate_no_onnx`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- input_queue(입력 큐): `{rel(INPUT_QUEUE_PATH)}`",
            f"- input_audit(입력 감사): `{rel(INPUT_AUDIT_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- feature_diagnostics(피처 진단): `{rel(FEATURE_DIAGNOSTICS_PATH)}`",
            f"- model_score_table_audit(모델 점수표 감사): `{rel(MODEL_AUDIT_PATH)}`",
            f"- attempts(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267Q_internal_feature_order_confirmed_adapter_materialization`.",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.",
            "- evidence_available(있는 근거): feature/model/set/ini(피처/모델/설정/초기화), Common Files copy(Common Files 복사), manifest(목록), hash(해시).",
            "- evidence_missing(없는 근거): MT5 execution(MT5 실행), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표).",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    judgment = "materialized_execution_pending_no_candidate_selection"
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267Q_internal_feature_order_confirmed_adapter_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "internal_feature_order_confirmed_adapter_materialization",
            "tier_scope": "Tier A and actual routed total attempts planned",
            "scoreboard": "feature_model_set_ini_manifest",
            "status": STATUS,
            "judgment": judgment,
            "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION};selected_candidate=none.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "internal_feature_order_confirmed_adapter_materialization",
            "status": STATUS,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267Q materializes P0 internal adapter feature-order candidates; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__internal_feature_order_confirmed_adapter_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "internal_feature_order_confirmed_adapter_materialization",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "internal_feature_order_confirmed_adapter_materialization",
            "tier_scope": "Tier A and actual routed total attempts planned",
            "kpi_scope": "feature_model_set_ini_manifest_only",
            "scoreboard_lane": "adapter_materialization",
            "status": STATUS,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable_materialization_pending_mt5_execution",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    entries = (
        ("stage267_run267Q_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267Q internal adapter materialization."),
        ("stage267_run267Q_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267Q internal adapter variant manifest."),
        ("stage267_run267Q_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267Q runtime contract."),
        ("stage267_run267Q_feature_diagnostics", "feature_diagnostics", FEATURE_DIAGNOSTICS_PATH, "Run267Q feature diagnostics."),
        ("stage267_run267Q_model_score_table_audit", "model_score_table_audit", MODEL_AUDIT_PATH, "Run267Q model score table audit."),
        ("stage267_run267Q_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267Q MT5 attempt manifest."),
        ("stage267_run267Q_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267Q run manifest."),
        ("stage267_run267Q_lineage", "lineage", LINEAGE_PATH, "Run267Q artifact lineage."),
        ("stage267_run267Q_result", "result", RESULT_PATH, "Run267Q result payload."),
        ("stage267_run267Q_report", "review_report", REPORT_PATH, "User-facing run267Q materialization report."),
    )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_docs(result: Mapping[str, Any]) -> None:
    review_line = f"- Stage267(267단계) run267Q internal feature order confirmed Adapter materialization(내부 피처 순서 확인 어댑터 물질화): `{rel(REPORT_PATH)}`"
    index_line = f"- run267Q_internal_feature_order_confirmed_adapter_materialization(267Q 내부 피처 순서 확인 어댑터 물질화): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267Q(267Q 실행)는 run267P(267P 실행)의 P0 Adapter design queue(P0 어댑터 설계 큐)를 "
        "feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.\n"
        "Effect(효과): next action(다음 행동)은 MT5(MetaTrader 5, 메타트레이더5) 실행이며 selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 없다."
    )
    for path, line, anchor in (
        (CURRENT_WORKING_STATE_PATH, review_line, "stage267_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.md"),
        (SELECTION_STATUS_PATH, index_line, "run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design"),
        (REVIEW_INDEX_PATH, index_line, "run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design"),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `internal_feature_order_confirmed_adapter_materialization`")
            text = replace_existing_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "## Current Next Action",
                f"- latest_materialization(최신 물질화): run267Q(267Q 실행) variants(변형) `{result['variant_count']}`, attempts(시도) `{result['attempt_count']}`, report(보고서) `{rel(REPORT_PATH)}`.",
            )
            text = replace_line_prefix(
                text,
                "- action(행동):",
                "- action(행동): run267Q(267Q 실행)는 run267P(267P 실행)의 P0 Adapter design queue(P0 어댑터 설계 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(효과):",
                "- effect(효과): 다음 작업은 물질화된 내부 Adapter(어댑터) 후보를 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 curve/time-slice/trade quality(곡선/시간구간/거래 품질)를 확인하는 것이다.",
            )
        elif path == SELECTION_STATUS_PATH:
            text = replace_existing_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        else:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, anchor, line)
        text = append_after_contains(text, "Run267P(267P 실행)는", summary_line)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("status: run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design_completed", f"status: {STATUS}")
    workspace = workspace.replace(f"last_completed_run_id: {SOURCE_RUN_ID}", f"last_completed_run_id: {RUN_ID}")
    workspace = workspace.replace("next_action: run267Q_materialize_internal_feature_order_confirmed_adapter_candidates", f"next_action: {NEXT_ACTION}")
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267Q_materialize_internal_feature_order_confirmed_adapter_candidates`이다. Effect(효과): 내부 feature order(피처 순서)가 확인된 Adapter(어댑터) 후보만 다음 물질화 후보로 좁힌다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 물질화된 내부 Adapter(어댑터) 후보를 MT5(MetaTrader 5, 메타트레이더5)에서 실행한다.",
    )
    workspace = workspace.replace(
        "is active_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design_completed(267P 내부 피처 순서 확인 및 어댑터 설계 완료, 내부 피처 물질화 대기 활성).",
        "is active_run267Q_internal_feature_order_confirmed_adapter_materialized_execution_pending(267Q 내부 피처 순서 확인 어댑터 물질화 완료, MT5 실행 대기 활성).",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267Q(267Q 실행) internal feature order confirmed Adapter materialization(내부 피처 순서 확인 어댑터 물질화) `{STATUS}`. Effect(효과): run267P(267P 실행)의 P0 volatility/ATR(변동성/ATR) Adapter design queue(어댑터 설계 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 고정했고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    workspace = append_after_contains(
        workspace,
        "run267P_internal_feature_order_confirmation_adapter_design_report_path",
        f"  run267Q_internal_feature_order_confirmed_adapter_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def materialize() -> dict[str, Any]:
    payload = materialize_payload()
    result = write_outputs(payload)
    update_ledgers(str(payload["created_at_utc"]), result)
    update_current_docs(result)
    return result


def main() -> None:
    result = materialize()
    print(
        json.dumps(
            {
                "status": result["status"],
                "run_id": result["run_id"],
                "variant_count": result["variant_count"],
                "attempt_count": result["attempt_count"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
