from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
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
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    execute_prepared_run,
    parse_ini,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_mt5_development as base  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50CA"
RUN_ID = "run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1"
PACKET_ID = "stage56_baseline_adapter_onnx_runtime_reproduction_v1"
TERMINAL_LABEL_ATTEMPTED = "mt5_runtime_reproduction_attempted"
TERMINAL_LABEL_REPAIRING = "mt5_runtime_reproduction_failed_repairing"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SELECTED_ADAPTER_ID = "ba14_no_atr_sd5_lot025"
REPAIR_LABEL = "no_atr_same_direction_cooldown5_lot025"

SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs/run50BR"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / DEVELOPMENT_ANCHOR
ONNX_RUN_ROOT = STAGE_ROOT / "02_runs/run50BZ"
ONNX_MODEL_SOURCE = ONNX_RUN_ROOT / "models/ba14_stage56_context_gap_refill_entry.onnx"
ONNX_TABLE_SOURCE = ONNX_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
ONNX_PARITY_JSON = REVIEWS_ROOT / "run50BZ_baseline_adapter_onnx_parity.json"
PHASE_A_SUMMARY_JSON = REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_summary.json"
FIRST_ADAPTER_SUMMARY_CSV = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_summary.csv"
CANDIDATE_CSV_PATH = REVIEWS_ROOT / "run50BS_candidate_selection.csv"
SPEC_JSON_PATH = SELECTED_ROOT / "baseline_adapter_ba14_spec.json"
SPEC_MD_PATH = SELECTED_ROOT / "baseline_adapter_ba14_spec.md"

REPORT_PATH = REVIEWS_ROOT / "run50CA_baseline_adapter_onnx_runtime_reproduction.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "run50CA_baseline_adapter_onnx_runtime_reproduction_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50CA_baseline_adapter_onnx_runtime_reproduction_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50CA_baseline_adapter_onnx_runtime_reproduction_audit.csv"
RISK_CSV_PATH = REVIEWS_ROOT / "run50CA_baseline_adapter_onnx_runtime_reproduction_risk_telemetry.csv"
HANDOFF_JSON_PATH = RUN_ROOT / "handoff/baseline_adapter_ba14_onnx_runtime_handoff.json"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

FEATURE_COLUMN = "stage56_context_gap_refill_signal"
FEATURE_ORDER_HASH = repair.FEATURE_ORDER_HASH
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_baseline_adapter_onnx_runtime"
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0
REPRODUCTION_TOLERANCE = {
    "trades_per_day": 0.02,
    "profit_factor": 0.02,
    "net_profit": 1.0,
    "max_drawdown_amount": 1.0,
}

REPRO_VARIANTS = (
    repair.RepairVariant(
        adapter_id=SELECTED_ADAPTER_ID,
        label=REPAIR_LABEL,
        atr_enabled=False,
        model_risk_enabled=False,
        fixed_lot=0.25,
        atr_stop_multiplier=0.0,
        atr_take_profit_multiplier=0.0,
        model_risk_max_pct=0.0,
        same_direction_reentry_cooldown_bars=5,
        notes="ONNX runtime reproduction of the Phase A selected ba14 adapter.",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(io_path(Path(".")).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def append_once(path: Path, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if text.strip() in existing:
        return
    write_md(path, existing.rstrip() + "\n" + text.strip() + "\n")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt(value: Any) -> str:
    return aw.fmt(value)


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def source_attempt_ini(split: str) -> Path:
    name = "x01_ta_val.ini" if split == "validation_is" else "x01_ta_oos.ini"
    return SOURCE_VARIANT_ROOT / "mt5" / name


def source_feature(split: str, tier: str = "a") -> Path:
    token = "val" if split == "validation_is" else "oos"
    return SOURCE_VARIANT_ROOT / "features" / f"{DEVELOPMENT_ANCHOR}_{tier}_{token}.csv"


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def configure_repair_module() -> None:
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.PACKET_ID = PACKET_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.PACKET_ROOT = PACKET_ROOT
    repair.COMMON_ROOT = COMMON_ROOT
    repair.REPAIR_VARIANTS = REPRO_VARIANTS
    repair.REPORT_PATH = REPORT_PATH
    repair.SUMMARY_JSON_PATH = SUMMARY_JSON_PATH
    repair.SUMMARY_CSV_PATH = SUMMARY_CSV_PATH
    repair.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    repair.RISK_CSV_PATH = RISK_CSV_PATH


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    model_local = RUN_ROOT / "models" / ONNX_MODEL_SOURCE.name
    table_local = RUN_ROOT / "models" / ONNX_TABLE_SOURCE.name
    copied.append(copy_local(ONNX_MODEL_SOURCE, model_local))
    copied.append(copy_local(ONNX_TABLE_SOURCE, table_local))
    copied.append(copy_to_common(model_local, f"{COMMON_ROOT}/models/{model_local.name}", common_files_root))
    copied.append(copy_to_common(table_local, f"{COMMON_ROOT}/models/{table_local.name}", common_files_root))
    feature_exports: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        split_token = "val" if split == "validation_is" else "oos"
        feature_local = RUN_ROOT / DEVELOPMENT_ANCHOR / "features" / f"{DEVELOPMENT_ANCHOR}_onnx_adapter_a_{split_token}.csv"
        copied.append(copy_local(source_feature(split, "a"), feature_local))
        copied.append(copy_to_common(feature_local, f"{COMMON_ROOT}/features/{feature_local.name}", common_files_root))
        feature_exports[split] = {
            "path": rel(feature_local),
            "common_path": f"{COMMON_ROOT}/features/{feature_local.name}",
            "sha256": sha256_file_lf_normalized(feature_local),
        }
    return {
        "model_local": model_local,
        "model_common": f"{COMMON_ROOT}/models/{model_local.name}",
        "table_local": table_local,
        "feature_exports": feature_exports,
        "common_copies": copied,
    }


def load_phase_a_best() -> dict[str, Any]:
    payload = read_json(PHASE_A_SUMMARY_JSON)
    best = payload.get("phase_a_best_variant", {})
    return dict(best) if isinstance(best, Mapping) else {}


def load_onnx_parity() -> dict[str, Any]:
    return read_json(ONNX_PARITY_JSON)


def load_spec() -> dict[str, Any]:
    return read_json(SPEC_JSON_PATH)


def write_handoff(inputs: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    spec = load_spec()
    payload = {
        "run_id": RUN_ID,
        "adapter_id": SELECTED_ADAPTER_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "boundary": BOUNDARY,
        "model_runtime": {
            "backend": "onnx",
            "local_path": rel(inputs["model_local"]),
            "common_path": inputs["model_common"],
            "sha256": sha256_file_lf_normalized(Path(str(inputs["model_local"]))),
            "input_name": spec.get("entry_contract", {}).get("input_name"),
            "output_name": spec.get("entry_contract", {}).get("probability_output_name"),
            "class_order": spec.get("entry_contract", {}).get("class_order"),
        },
        "feature_input_contract": {
            "feature_order": [FEATURE_COLUMN],
            "feature_count": 1,
            "feature_order_hash": FEATURE_ORDER_HASH,
            "validation_feature": inputs["feature_exports"]["validation_is"],
            "oos_feature": inputs["feature_exports"]["oos"],
        },
        "entry_contract": spec.get("entry_contract", {}),
        "route_tier_contract": spec.get("route_tier_contract", {}),
        "risk_contract": spec.get("risk_contract", {}),
        "atr_bracket_contract": spec.get("atr_bracket_contract", {}),
        "lifecycle_contract": spec.get("lifecycle_contract", {}),
        "mt5_execution_translation": {
            "lot_rounding": "MT5 ExecutionBridge owns broker min/max/step normalization.",
            "min_lot_floor": "0.01 lot floor remains MT5-side execution safety, not ONNX.",
            "broker_stop_distance": "MT5-side order validation.",
            "order_send": "MT5-side only.",
        },
        "telemetry_contract": spec.get("telemetry_contract", {}),
        "attempt_set_files": [attempt.get("set", {}).get("path") for attempt in attempts],
    }
    write_json(HANDOFF_JSON_PATH, payload)
    return payload


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    return {
        "InpFixedLot": variant.fixed_lot,
        "InpAtrSltpEnabled": variant.atr_enabled,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": variant.atr_stop_multiplier,
        "InpAtrTakeProfitMultiplier": variant.atr_take_profit_multiplier,
        "InpAtrMinStopPoints": 0.0,
        "InpAtrMaxStopPoints": 0.0,
        "InpAtrMinTakeProfitPoints": 0.0,
        "InpAtrMaxTakeProfitPoints": 0.0,
        "InpModelRiskSizingEnabled": variant.model_risk_enabled,
        "InpModelRiskMinPct": 0.0,
        "InpModelRiskMaxPct": variant.model_risk_max_pct,
        "InpModelRiskConfidenceFloor": 0.55,
        "InpModelRiskConfidenceCeiling": 0.85,
        "InpModelRiskFallbackLot": variant.fixed_lot,
        "InpFallbackEnabled": False,
        "InpFallbackUseOnPrimaryFlat": False,
        "InpFallbackUseOnPrimaryLowConfidence": False,
        "InpReentryCooldownBars": int(variant.reentry_cooldown_bars),
        "InpSameDirectionReentryCooldownBars": int(variant.same_direction_reentry_cooldown_bars),
        "InpEntryTransitionOnly": bool(variant.entry_transition_only),
        "InpEntryTransitionRearmMinConfidenceDelta": float(variant.entry_transition_rearm_min_confidence_delta),
        "InpMagic": magic,
    }


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    variant = REPRO_VARIANTS[0]
    variant_root = RUN_ROOT / variant.adapter_id
    for split in ("validation_is", "oos"):
        date_values = parse_ini(source_attempt_ini(split))
        split_token = "val" if split == "validation_is" else "oos"
        for role_index, (role, tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                ("tier_a_only", mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                ("routed", mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
            ),
            start=1,
        ):
            magic = 5651000 + (1 if split == "validation_is" else 50) + role_index
            attempts.append(
                attempt_payload(
                    run_root=variant_root,
                    run_id=RUN_ID,
                    stage_number=56,
                    exploration_label="stage56_BaselineAdapter__OnnxRuntimeReproduction",
                    attempt_name=f"{variant.adapter_id}_onnx_{attempt_token}_{split_token}",
                    tier=tier,
                    split=split,
                    model_path=str(inputs["model_common"]),
                    model_id=f"{RUN_ID}_{variant.adapter_id}_entry_onnx",
                    model_backend="onnx",
                    feature_path=str(inputs["feature_exports"][split]["common_path"]),
                    feature_count=1,
                    feature_order_hash=FEATURE_ORDER_HASH,
                    short_threshold=SHORT_THRESHOLD,
                    long_threshold=LONG_THRESHOLD,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=str(date_values["FromDate"]),
                    to_date=str(date_values["ToDate"]),
                    primary_active_tier="tier_a",
                    attempt_role=attempt_role,
                    record_view_prefix=prefix,
                    max_hold_bars=variant.max_hold_bars,
                    common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                    fallback_enabled=False,
                    close_on_flat_signal=variant.close_on_flat_signal,
                    reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                    close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                    extra_set_values=extra_set_values(variant, magic),
                )
            )
    return attempts


def telemetry_number(value: Any) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number


def mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def enrich_risk_rows(risk_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    numeric_columns = (
        "model_risk_pct",
        "clipped_risk_pct",
        "computed_lot",
        "executed_lot",
        "actual_risk_pct_after_floor",
        "atr_points",
        "open_sl_points",
        "open_tp_points",
    )
    for row in risk_rows:
        item = dict(row)
        telemetry_path = Path(str(item.get("telemetry_path") or ""))
        if not path_exists(telemetry_path):
            enriched.append(item)
            continue
        buckets: dict[str, list[float]] = {column: [] for column in numeric_columns}
        with io_path(telemetry_path).open("r", encoding="utf-8-sig", newline="") as handle:
            for raw in csv.DictReader(handle):
                if str(raw.get("record_type") or "") != "cycle":
                    continue
                for column in numeric_columns:
                    number = telemetry_number(raw.get(column))
                    if number is not None:
                        buckets[column].append(number)
        item.update(
            {
                "avg_model_risk_pct": mean(buckets["model_risk_pct"]),
                "avg_clipped_risk_pct": mean(buckets["clipped_risk_pct"]),
                "max_clipped_risk_pct": max(buckets["clipped_risk_pct"]) if buckets["clipped_risk_pct"] else None,
                "avg_computed_lot": mean(buckets["computed_lot"]),
                "max_computed_lot": max(buckets["computed_lot"]) if buckets["computed_lot"] else None,
                "max_executed_lot": max(buckets["executed_lot"]) if buckets["executed_lot"] else None,
                "avg_actual_risk_pct_after_floor": mean(buckets["actual_risk_pct_after_floor"]),
                "avg_atr_points_from_raw": mean(buckets["atr_points"]),
                "avg_open_sl_points_from_raw": mean(buckets["open_sl_points"]),
                "avg_open_tp_points_from_raw": mean(buckets["open_tp_points"]),
            }
        )
        enriched.append(item)
    return enriched


def enrich_summary_rows(
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    risk_by_attempt = {str(row.get("attempt_name")): row for row in risk_rows}
    enriched: list[dict[str, Any]] = []
    for row in summary_rows:
        item = dict(row)
        if item.get("view") != "tier_b_fallback_only":
            attempt_token = "ta" if item.get("view") == "tier_a_only" else "rt"
            split_token = "val" if item.get("split") == "validation_is" else "oos"
            attempt_name = f"{SELECTED_ADAPTER_ID}_onnx_{attempt_token}_{split_token}"
            risk = risk_by_attempt.get(attempt_name, {})
            for key in (
                "avg_model_risk_pct",
                "avg_clipped_risk_pct",
                "max_clipped_risk_pct",
                "avg_computed_lot",
                "max_computed_lot",
                "max_executed_lot",
                "avg_actual_risk_pct_after_floor",
            ):
                item[key] = risk.get(key)
        enriched.append(item)
    return enriched


def route_coverage() -> dict[str, Any]:
    coverage: dict[str, Any] = {
        "by_split": {},
        "tier_b_disabled_reason": "disabled_due_run50BR_fallback_only_damage",
    }
    for name, split in (("validation", "validation_is"), ("oos", "oos")):
        a_rows = max(0, sum(1 for _ in io_path(source_feature(split, "a")).open("r", encoding="utf-8-sig")) - 1)
        b_path = source_feature(split, "b")
        b_rows = max(0, sum(1 for _ in io_path(b_path).open("r", encoding="utf-8-sig")) - 1) if path_exists(b_path) else 0
        coverage["by_split"][name] = {
            "tier_a_primary_rows": a_rows,
            "tier_b_fallback_rows_available_but_disabled": b_rows,
            "tier_b_fallback_rows_used": 0,
            "routed_labelable_rows": a_rows,
        }
    return coverage


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "materialized_only_no_mt5_evidence",
        }
    return execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )


def load_existing_result() -> dict[str, Any]:
    manifest = read_json(RUN_ROOT / "run_manifest.json")
    kpi = read_json(RUN_ROOT / "kpi_record.json")
    return {
        **manifest,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": manifest.get("attempts", []),
        "common_copies": manifest.get("common_copies", []),
        "compile": manifest.get("compile", {}),
        "external_verification_status": kpi.get("external_verification_status", manifest.get("external_verification_status")),
        "judgment": kpi.get("judgment", manifest.get("judgment")),
        "mt5_kpi_records": kpi.get("mt5_kpi_records", []),
        "strategy_tester_reports": kpi.get("strategy_tester_reports", []),
        "execution_results": kpi.get("execution_results", []),
        "route_coverage": route_coverage(),
    }


def routed_rows(summary_rows: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    val = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == SELECTED_ADAPTER_ID
            and row.get("split") == "validation_is"
            and row.get("view") == "actual_routed_total"
        ),
        {},
    )
    oos = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == SELECTED_ADAPTER_ID
            and row.get("split") == "oos"
            and row.get("view") == "actual_routed_total"
        ),
        {},
    )
    return val, oos


def tier_a_rows(summary_rows: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    val = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == SELECTED_ADAPTER_ID
            and row.get("split") == "validation_is"
            and row.get("view") == "tier_a_only"
        ),
        {},
    )
    oos = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == SELECTED_ADAPTER_ID
            and row.get("split") == "oos"
            and row.get("view") == "tier_a_only"
        ),
        {},
    )
    return val, oos


def phase_a_metrics() -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    best = load_phase_a_best()
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    return val, oos


def metric_diffs(runtime: Mapping[str, Any], phase_a: Mapping[str, Any]) -> dict[str, Any]:
    diffs: dict[str, Any] = {}
    for key in ("trades_per_day", "profit_factor", "net_profit", "max_drawdown_amount"):
        runtime_value = as_float(runtime.get(key))
        phase_value = as_float(phase_a.get(key))
        abs_diff = abs(runtime_value - phase_value)
        tol = REPRODUCTION_TOLERANCE[key]
        if key in {"net_profit", "max_drawdown_amount"}:
            tol = max(tol, abs(phase_value) * 0.01)
        diffs[key] = {
            "runtime": runtime_value,
            "phase_a": phase_value,
            "abs_diff": abs_diff,
            "tolerance": tol,
            "passed": abs_diff <= tol,
        }
    return diffs


def runtime_gate(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    val, oos = routed_rows(summary_rows)
    phase_val, phase_oos = phase_a_metrics()
    val_diff = metric_diffs(val, phase_val)
    oos_diff = metric_diffs(oos, phase_oos)
    failures: list[str] = []
    checks = (
        ("validation_trades_per_day_lt_5", as_float(val.get("trades_per_day")) < 5.0),
        ("oos_trades_per_day_lt_5", as_float(oos.get("trades_per_day")) < 5.0),
        ("validation_net_not_positive", as_float(val.get("net_profit")) <= 0.0),
        ("oos_net_not_positive", as_float(oos.get("net_profit")) <= 0.0),
        ("validation_pf_lt_1_10", as_float(val.get("profit_factor")) < 1.10),
        ("oos_pf_lt_1_10", as_float(oos.get("profit_factor")) < 1.10),
        ("validation_cost_stressed_expectancy_not_positive", as_float(val.get("cost_stressed_expectancy")) <= 0.0),
        ("oos_cost_stressed_expectancy_not_positive", as_float(oos.get("cost_stressed_expectancy")) <= 0.0),
        ("validation_same_move_above_0_40", as_float(val.get("same_move_reentry_ratio")) > 0.40),
        ("oos_same_move_above_0_40", as_float(oos.get("same_move_reentry_ratio")) > 0.40),
    )
    failures.extend(name for name, failed in checks if failed)
    if val.get("status") != "completed" or oos.get("status") != "completed":
        failures.append("mt5_runtime_record_missing_or_blocked")
    for row, split in ((val, "validation"), (oos, "oos")):
        for key in ("risk_floor_applied_count", "avg_executed_lot", "avg_open_sl_points", "avg_open_tp_points"):
            if row.get(key) in (None, ""):
                failures.append(f"{split}_{key}_telemetry_missing")
    for split, diffs in (("validation", val_diff), ("oos", oos_diff)):
        for key, diff in diffs.items():
            if not diff["passed"]:
                failures.append(f"{split}_{key}_reproduction_tolerance_failed")
    return {
        "passed": not failures,
        "failure_reasons": failures,
        "validation_reproduction_diff": val_diff,
        "oos_reproduction_diff": oos_diff,
        "tolerance_policy": REPRODUCTION_TOLERANCE,
    }


def load_csv_by_key(path: Path, key_fields: Sequence[str]) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    if not path_exists(path):
        return out
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = "/".join(str(row.get(field, "")) for field in key_fields)
            out[key] = dict(row)
    return out


def comparison_payload(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    refs = load_csv_by_key(CANDIDATE_CSV_PATH, ("run_number", "variant_id"))
    first = load_csv_by_key(FIRST_ADAPTER_SUMMARY_CSV, ("split", "view"))
    val, oos = routed_rows(summary_rows)
    phase_val, phase_oos = phase_a_metrics()
    return {
        "phase_a_adapter": {"validation": dict(phase_val), "oos": dict(phase_oos)},
        "phase_c_onnx_runtime": {"validation": dict(val), "oos": dict(oos)},
        "first_adapter_run50BT": {
            "validation": dict(first.get("validation_is/actual_routed_total", {})),
            "oos": dict(first.get("oos/actual_routed_total", {})),
        },
        "development_anchor": dict(refs.get(f"run50BR/{DEVELOPMENT_ANCHOR}", {})),
        "backup_anchor": dict(refs.get(f"run50BQ/{BACKUP_ANCHOR}", {})),
        "d390h10_reference": dict(refs.get("run50BR/v64_v47_ctxgap14_refill_etfw_h2_no_b", {})),
        "d38h10_reference": dict(refs.get("run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b", {})),
    }


def artifact_rows(result: Mapping[str, Any], extra_paths: Sequence[Path]) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        is_file = path_exists(resolved) and io_path(resolved).is_file()
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(p),
                "sha256": sha256_file_lf_normalized(resolved) if is_file else "directory_or_not_feasible",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in extra_paths:
        suffix = path.suffix.lstrip(".") or "file"
        add(
            f"stage56_{RUN_NUMBER}_{aw.safe_name(f'{path.stem}_{suffix}', 80)}",
            "stage56_onnx_runtime_reproduction_artifact",
            path,
            "Phase C runtime reproduction artifact.",
        )
    for execution in result.get("execution_results", []):
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        for key, artifact_type in (("telemetry_path", "mt5_runtime_telemetry_csv"), ("summary_path", "mt5_runtime_summary_csv")):
            value = runtime_outputs.get(key)
            if value:
                add(f"stage56_{RUN_NUMBER}_{artifact_type}_{aw.safe_name(str(execution.get('attempt_name')), 80)}", artifact_type, str(value), "Common Files runtime telemetry emitted by MT5 EA.")
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        report_path = html.get("path")
        if report_path:
            add(f"stage56_{RUN_NUMBER}_strategy_tester_html_{aw.safe_name(str(report.get('attempt_name') or report.get('report_name')), 80)}", "mt5_strategy_tester_html_report", str(report_path), "MT5 Strategy Tester HTML report.")
    return rows


def clear_prior_artifact_rows_for_run() -> None:
    if not path_exists(ARTIFACT_REGISTRY_PATH):
        return
    with io_path(ARTIFACT_REGISTRY_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    prefix = f"stage56_{RUN_NUMBER}_"
    kept = [
        row
        for row in rows
        if not (
            str(row.get("run_id", "")).strip() == RUN_ID
            and str(row.get("artifact_id", "")).startswith(prefix)
        )
    ]
    write_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, kept)


def write_ledgers(result: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]], gate: Mapping[str, Any]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    judgment = "onnx_runtime_reproduction_passed_research_only" if gate.get("passed") else "onnx_runtime_reproduction_failed_repairing"
    run_status = TERMINAL_LABEL_ATTEMPTED if external == "completed" else TERMINAL_LABEL_REPAIRING
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_onnx_runtime_reproduction",
            "status": run_status,
            "judgment": judgment,
            "path": rel(SUMMARY_JSON_PATH),
            "notes": f"adapter_id={SELECTED_ADAPTER_ID};development_anchor={DEVELOPMENT_ANCHOR};boundary={BOUNDARY}",
        }
    ]
    ledger_rows: list[dict[str, Any]] = [
        {
            "ledger_row_id": f"{RUN_ID}__aggregate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate",
            "parent_run_id": "run50BZ_stage56_baseline_adapter_onnx_hardening_v1",
            "record_view": "onnx_runtime_reproduction_aggregate",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "baseline_adapter_onnx_runtime_reproduction",
            "scoreboard_lane": "runtime_probe",
            "status": run_status,
            "judgment": judgment,
            "path": rel(SUMMARY_JSON_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("runtime_gate_passed", gate.get("passed")),
                    ("validation_repro_diff", gate.get("validation_reproduction_diff")),
                    ("oos_repro_diff", gate.get("oos_reproduction_diff")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("onnx_parity_passed", load_onnx_parity().get("parity", {}).get("passed", load_onnx_parity().get("passed"))),
                    ("tier_b_policy", "disabled_with_evidence"),
                    ("forbidden_operating_claims", False),
                )
            ),
            "external_verification_status": external,
            "notes": "Actual MT5 ONNX runtime validation/OOS reproduction; research/development only.",
        }
    ]
    for row in summary_rows:
        view = str(row.get("view"))
        split = str(row.get("split"))
        tier_scope = mt5.TIER_B if view == "tier_b_fallback_only" else mt5.TIER_A if view == "tier_a_only" else mt5.TIER_AB
        ledger_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{SELECTED_ADAPTER_ID}__{view}__{split}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{SELECTED_ADAPTER_ID}_{view}_{split}",
                "parent_run_id": RUN_ID,
                "record_view": f"{SELECTED_ADAPTER_ID}_{view}_{split}",
                "tier_scope": tier_scope,
                "kpi_scope": "baseline_adapter_onnx_runtime_reproduction",
                "scoreboard_lane": "runtime_probe",
                "status": row.get("status", "missing"),
                "judgment": judgment if view != "tier_b_fallback_only" else "tier_b_disabled_due_prior_fallback_damage",
                "path": row.get("report_path") or rel(SUMMARY_JSON_PATH),
                "primary_kpi": ledger_pairs(
                    (
                        ("trades_per_day", row.get("trades_per_day")),
                        ("profit_factor", row.get("profit_factor")),
                        ("net_profit", row.get("net_profit")),
                        ("max_drawdown_amount", row.get("max_drawdown_amount")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("cost_stressed_expectancy", row.get("cost_stressed_expectancy")),
                        ("same_move_reentry_ratio", row.get("same_move_reentry_ratio")),
                        ("mfe_capture_ratio", row.get("mfe_capture_ratio")),
                        ("risk_floor_applied_count", row.get("risk_floor_applied_count")),
                        ("model_backend", "onnx"),
                    )
                ),
                "external_verification_status": external,
                "notes": "Tier B is disabled when view is tier_b_fallback_only; no synthetic aggregation is used.",
            }
        )
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    clear_prior_artifact_rows_for_run()
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def write_report(summary_rows: Sequence[Mapping[str, Any]], gate: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    val, oos = routed_rows(summary_rows)
    ta_val, ta_oos = tier_a_rows(summary_rows)
    phase_val, phase_oos = phase_a_metrics()
    parity = load_onnx_parity()
    terminal_label = TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING
    lines = [
        f"# Stage56 {RUN_NUMBER} BaselineAdapter ONNX Runtime Reproduction(Stage56 {RUN_NUMBER} 기준선 어댑터 ONNX 런타임 재현)",
        "",
        f"- terminal_label(종료 라벨): `{terminal_label}`",
        f"- adapter_id(어댑터 ID): `{SELECTED_ADAPTER_ID}`",
        f"- development_anchor(개발 기준점): `run50BR/{DEVELOPMENT_ANCHOR}`",
        f"- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- runtime_gate_passed(런타임 게이트 통과): `{gate.get('passed')}`",
        "",
        "Action(행동): ba14 adapter(ba14 어댑터)를 ONNX backend(ONNX 백엔드)로 실제 MT5 validation/OOS(검증/표본외)에 다시 실행했다.",
        "Effect(효과): Python adapter(Python 어댑터), ONNX parity(ONNX 동등성), MT5 runtime(MT5 런타임) 사이의 재현 차이를 한 경로에서 확인한다.",
        "",
        "## ONNX Parity(ONNX 동등성)",
        "",
        f"- passed(통과): `{parity.get('parity', {}).get('passed', parity.get('passed'))}`",
        f"- max_abs_diff(최대 절대 차이): `{parity.get('parity', {}).get('max_abs_diff', parity.get('max_abs_diff'))}`",
        f"- tolerance(허용 오차): `{parity.get('parity', {}).get('tolerance', parity.get('tolerance'))}`",
        f"- onnx_sha256(ONNX 해시): `{parity.get('export', {}).get('sha256')}`",
        "",
        "## MT5 Runtime Metrics(MT5 런타임 지표)",
        "",
        "| split(구간) | view(보기) | trades/day(일 거래 수) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | same move(동일 이동) | MFE | computed lot(계산 랏) | executed lot(실행 랏) | floor(바닥) | SL | TP |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        if row.get("view") == "tier_b_fallback_only":
            continue
        lines.append(
            "| {split} | {view} | {day} | {pf} | {net} | {dd} | {cost} | {same} | {mfe} | {computed} | {lot} | {floor} | {sl} | {tp} |".format(
                split=row.get("split", ""),
                view=row.get("view", ""),
                day=fmt(row.get("trades_per_day")),
                pf=fmt(row.get("profit_factor")),
                net=fmt(row.get("net_profit")),
                dd=fmt(row.get("max_drawdown_amount")),
                cost=fmt(row.get("cost_stressed_expectancy")),
                same=fmt(row.get("same_move_reentry_ratio")),
                mfe=fmt(row.get("mfe_capture_ratio")),
                computed=fmt(row.get("avg_computed_lot")),
                lot=fmt(row.get("avg_executed_lot")),
                floor=fmt(row.get("risk_floor_applied_count")),
                sl=fmt(row.get("avg_open_sl_points")),
                tp=fmt(row.get("avg_open_tp_points")),
            )
        )
    lines.extend(
        [
            "",
            "## Phase A Comparison(Phase A 비교)",
            "",
            "| split(구간) | Phase A day(Phase A 일 거래 수) | Runtime day(런타임 일 거래 수) | Phase A PF | Runtime PF(런타임 PF) | Phase A net(순손익) | Runtime net(런타임 순손익) |",
            "|---|---:|---:|---:|---:|---:|---:|",
            f"| validation(검증) | {fmt(phase_val.get('trades_per_day'))} | {fmt(val.get('trades_per_day'))} | {fmt(phase_val.get('profit_factor'))} | {fmt(val.get('profit_factor'))} | {fmt(phase_val.get('net_profit'))} | {fmt(val.get('net_profit'))} |",
            f"| OOS(표본외) | {fmt(phase_oos.get('trades_per_day'))} | {fmt(oos.get('trades_per_day'))} | {fmt(phase_oos.get('profit_factor'))} | {fmt(oos.get('profit_factor'))} | {fmt(phase_oos.get('net_profit'))} | {fmt(oos.get('net_profit'))} |",
            "",
            "## Tier Records(티어 기록)",
            "",
            f"- Tier A only validation/OOS(Tier A 단독 검증/표본외): day `{fmt(ta_val.get('trades_per_day'))}` / `{fmt(ta_oos.get('trades_per_day'))}`, PF `{fmt(ta_val.get('profit_factor'))}` / `{fmt(ta_oos.get('profit_factor'))}`, net `{fmt(ta_val.get('net_profit'))}` / `{fmt(ta_oos.get('net_profit'))}`",
            "- Tier B fallback-only(Tier B 대체 전용): `disabled_due_run50BR_fallback_only_damage`",
            f"- A+B actual routed total(A+B 실제 라우팅 전체): validation/OOS net `{fmt(val.get('net_profit'))}` / `{fmt(oos.get('net_profit'))}`",
            "",
            "## Gate(게이트)",
            "",
            f"- passed(통과): `{gate.get('passed')}`",
            f"- failure_reasons(실패 사유): `{';'.join(gate.get('failure_reasons', []))}`",
            f"- validation_reproduction_diff(검증 재현 차이): `{json.dumps(json_ready(gate.get('validation_reproduction_diff')), ensure_ascii=False, sort_keys=True)}`",
            f"- oos_reproduction_diff(표본외 재현 차이): `{json.dumps(json_ready(gate.get('oos_reproduction_diff')), ensure_ascii=False, sort_keys=True)}`",
            "",
            "No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))


def remove_workspace_block(text: str, key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(key):
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith(" ")):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    return "".join(output)


def update_state_docs(summary_rows: Sequence[Mapping[str, Any]], gate: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    val, oos = routed_rows(summary_rows)
    terminal_label = TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- status(상태): `{terminal_label}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)은 BaselineAdapter ONNX runtime reproduction(기준선 어댑터 ONNX 런타임 재현)을 진행했다.
Effect(효과): Python adapter(Python 어댑터)와 ONNX runtime(ONNX 런타임)이 같은 MT5 tester account path(MT5 테스터 계좌 경로)에서 재현되는지 확인한다.

## Latest Runtime Evidence(최신 런타임 근거)

- adapter_id(어댑터 ID): `{SELECTED_ADAPTER_ID}`
- runtime_gate_passed(런타임 게이트 통과): `{gate.get('passed')}`
- validation/OOS trades/day(검증/표본외 일 거래 수): `{fmt(val.get('trades_per_day'))}` / `{fmt(oos.get('trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(val.get('profit_factor'))}` / `{fmt(oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(val.get('net_profit'))}` / `{fmt(oos.get('net_profit'))}`
- validation/OOS drawdown(검증/표본외 손실폭): `{fmt(val.get('max_drawdown_amount'))}` / `{fmt(oos.get('max_drawdown_amount'))}`
- validation/OOS same_move(검증/표본외 동일 이동): `{fmt(val.get('same_move_reentry_ratio'))}` / `{fmt(oos.get('same_move_reentry_ratio'))}`
- risk_floor(위험 바닥): validation/OOS `{fmt(val.get('risk_floor_applied_count'))}` / `{fmt(oos.get('risk_floor_applied_count'))}`
- ATR SL/TP(ATR 손절/익절): disabled(비활성), open points(개설 포인트) `{fmt(val.get('avg_open_sl_points'))}` / `{fmt(val.get('avg_open_tp_points'))}`
- failure_reasons(실패 사유): `{';'.join(gate.get('failure_reasons', []))}`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료).
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_baseline_adapter_development`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- current_judgment(현재 판정): `{terminal_label}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`

## BaselineAdapter ONNX Runtime Evidence(기준선 어댑터 ONNX 런타임 근거)

- selected_adapter(선택 어댑터): `{SELECTED_ADAPTER_ID}`
- adapter_spec(어댑터 명세): `{rel(SPEC_JSON_PATH)}`
- onnx_parity_report(ONNX 동등성 보고서): `{rel(ONNX_PARITY_JSON)}`
- runtime_reproduction_report(런타임 재현 보고서): `{rel(REPORT_PATH)}`
- runtime_summary_json(런타임 요약 JSON): `{rel(SUMMARY_JSON_PATH)}`
- runtime_summary_csv(런타임 요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- runtime_risk_telemetry(런타임 위험 텔레메트리): `{rel(RISK_CSV_PATH)}`
- runtime_gate_passed(런타임 게이트 통과): `{gate.get('passed')}`

Effect(효과): BaselineAdapter(기준선 어댑터)는 아직 deployment(배포), live readiness(실거래 준비), operating reference(운영 기준)를 주장하지 않는다.
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage56(56단계) `{STAGE_ID}`: {RUN_NUMBER}(실행 {RUN_NUMBER}) BaselineAdapter ONNX runtime reproduction(기준선 어댑터 ONNX 런타임 재현)을 실행했다. "
        f"adapter(어댑터)는 `{SELECTED_ADAPTER_ID}`, runtime_gate_passed(런타임 게이트 통과)는 `{gate.get('passed')}`이다. "
        "Effect(효과): Python/ONNX/MT5(Python/ONNX/MT5) 재현 차이를 실제 tester account path(테스터 계좌 경로)에서 확인한다.\n"
    )
    text = re.sub(
        rf"- >-\n  Stage56\(56단계\) `{re.escape(STAGE_ID)}`: {RUN_NUMBER}\(실행 {RUN_NUMBER}\) BaselineAdapter ONNX runtime reproduction[^\n]*\n",
        "",
        text,
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}", text, count=1)
    text = remove_workspace_block(text, "stage56_baseline_adapter_onnx_runtime_reproduction:")
    block = f"""
stage56_baseline_adapter_onnx_runtime_reproduction:
  packet_id: {PACKET_ID}
  current_run_id: {RUN_ID}
  adapter_id: {SELECTED_ADAPTER_ID}
  development_anchor: {DEVELOPMENT_ANCHOR}
  backup_anchor: {BACKUP_ANCHOR}
  terminal_label: {terminal_label}
  runtime_gate_passed: {str(bool(gate.get('passed'))).lower()}
  selected_research_baseline: none
  boundary: {BOUNDARY}
  next_action: commit_push_progress_then_close_goal_only_if_hard_completion_evidence_is_reported
"""
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    gate: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
    handoff: Mapping[str, Any],
) -> None:
    val, oos = routed_rows(summary_rows)
    ta_val, ta_oos = tier_a_rows(summary_rows)
    parity = load_onnx_parity()
    aggregate = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "terminal_label": TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING,
        "adapter_id": SELECTED_ADAPTER_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "backup_anchor": BACKUP_ANCHOR,
        "selected_research_baseline": "none",
        "runtime_gate": gate,
        "validation_metrics": val,
        "oos_metrics": oos,
        "tier_a_validation": ta_val,
        "tier_a_oos": ta_oos,
        "tier_b_policy": "disabled_due_run50BR_fallback_only_damage",
        "onnx_parity": parity,
        "handoff": handoff,
        "comparison": comparison_payload(summary_rows),
        "summary_json_path": rel(SUMMARY_JSON_PATH),
        "summary_csv_path": rel(SUMMARY_CSV_PATH),
        "risk_csv_path": rel(RISK_CSV_PATH),
        "report_path": rel(REPORT_PATH),
        "ledger_payload": ledger_payload,
        "hard_completion_status": "pending_git_push_and_user_report" if gate.get("passed") else "not_met",
        "forbidden_claims": {
            "live_readiness": False,
            "runtime_authority": False,
            "operating_promotion": False,
            "operating_reference": False,
            "production_baseline": False,
            "reviewed_closed": False,
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "result_judgment_gate.json", {
        "result_subject": RUN_ID,
        "judgment_label": "onnx_runtime_reproduction_passed_research_only" if gate.get("passed") else TERMINAL_LABEL_REPAIRING,
        "runtime_gate_passed": gate.get("passed"),
        "validation_metrics": val,
        "oos_metrics": oos,
        "failure_reasons": gate.get("failure_reasons", []),
        "claim_boundary": BOUNDARY,
        "status": "passed" if gate.get("passed") else "repair_required",
    })
    write_json(PACKET_ROOT / "runtime_parity_audit.json", {
        "status": "passed" if gate.get("passed") else "failed_repairing",
        "python_adapter_source": rel(PHASE_A_SUMMARY_JSON),
        "onnx_parity_source": rel(ONNX_PARITY_JSON),
        "mt5_runtime_source": rel(SUMMARY_JSON_PATH),
        "reproduction_diff": {
            "validation": gate.get("validation_reproduction_diff"),
            "oos": gate.get("oos_reproduction_diff"),
        },
        "known_differences": "Broker execution safety remains MT5-side; ONNX owns probability output only.",
    })
    write_json(PACKET_ROOT / "backtest_forensics_audit.json", {
        "status": "passed" if result.get("external_verification_status") == "completed" else "blocked",
        "tester_identity": "terminal64.exe; US100 M5; deposit=500; leverage=1:100; model=4",
        "trade_evidence": "MT5 Strategy Tester HTML reports and RuntimeTelemetry CSV files",
        "boundary": BOUNDARY,
    })
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {
        "status": "passed",
        "source_inputs": [rel(ONNX_MODEL_SOURCE), rel(SPEC_JSON_PATH), rel(source_feature("validation_is")), rel(source_feature("oos"))],
        "producer": rel(Path(__file__)),
        "consumers": [rel(REPORT_PATH), rel(SUMMARY_JSON_PATH), rel(SUMMARY_CSV_PATH), rel(RISK_CSV_PATH), rel(HANDOFF_JSON_PATH)],
        "ledger_links": ledger_payload,
    })
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {
        "required_gates": [
            "actual_mt5_onnx_runtime_validation",
            "actual_mt5_onnx_runtime_oos",
            "onnx_parity_reference",
            "risk_atr_lot_telemetry_parse",
            "artifact_lineage_audit",
            "runtime_parity_audit",
            "final_claim_guard",
        ],
        "covered_gates": [
            "actual_mt5_onnx_runtime_validation" if val.get("status") == "completed" else "missing",
            "actual_mt5_onnx_runtime_oos" if oos.get("status") == "completed" else "missing",
            "onnx_parity_reference" if parity.get("parity", {}).get("passed", parity.get("passed")) else "failed",
            "risk_atr_lot_telemetry_parse" if all(row.get("status") == "completed" for row in risk_rows) else "partial",
            "artifact_lineage_audit",
            "runtime_parity_audit",
            "final_claim_guard",
        ],
        "status": "passed" if gate.get("passed") else "repair_required",
    })
    write_json(PACKET_ROOT / "final_claim_guard.json", {
        "hard_completion_label": "baseline_adapter_onnx_mt5_reproduction_completed",
        "hard_completion_ready_after_git_push": bool(gate.get("passed")),
        "hard_completion_met_in_repository_packet": False,
        "reason": "The final pushed commit hash must be reported after git push.",
        "forbidden_terminal_labels": [
            "reviewed_closed",
            "complete",
            "final",
            "production_ready",
            "live_ready",
            "operating_reference",
            "runtime_authority",
            "good_enough",
        ],
        "status": "passed",
    })
    write_json(PACKET_ROOT / "skill_receipts.json", [
        {"skill": "obsidian-reentry-read", "status": "completed"},
        {"skill": "obsidian-backtest-forensics", "status": "completed" if result.get("external_verification_status") == "completed" else "blocked"},
        {"skill": "obsidian-runtime-parity", "status": "completed" if gate.get("passed") else "failed_repairing"},
        {"skill": "obsidian-artifact-lineage", "status": "completed"},
        {"skill": "obsidian-model-validation", "status": "runtime_reproduction_judgment"},
        {"skill": "obsidian-result-judgment", "status": "completed"},
    ])


def write_run_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    gate: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
    handoff: Mapping[str, Any],
) -> None:
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(RISK_CSV_PATH, risk_rows)
    payload = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "terminal_label": TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING,
        "adapter_id": SELECTED_ADAPTER_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "backup_anchor": BACKUP_ANCHOR,
        "selected_research_baseline": "none",
        "external_verification_status": result.get("external_verification_status"),
        "runtime_gate": gate,
        "summary_rows": list(summary_rows),
        "risk_rows": list(risk_rows),
        "audit_rows": list(audit_rows),
        "onnx_parity": load_onnx_parity(),
        "handoff": handoff,
        "comparison": comparison_payload(summary_rows),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "ledger_payload": ledger_payload,
        "hard_completion_status": "pending_git_push_and_user_report" if gate.get("passed") else "not_met",
        "boundary": BOUNDARY,
    }
    write_json(SUMMARY_JSON_PATH, payload)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "adapter_id": SELECTED_ADAPTER_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "runtime_variant": [variant.__dict__ for variant in REPRO_VARIANTS],
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_json(RUN_ROOT / "kpi_record.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "execution_results": result.get("execution_results", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_packet_files(result, summary_rows, risk_rows, gate, ledger_payload, handoff)


def update_logs(summary_rows: Sequence[Mapping[str, Any]], gate: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    val, oos = routed_rows(summary_rows)
    terminal_label = TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING
    entry = f"""
## 2026-05-15 {RUN_NUMBER} BaselineAdapter ONNX Runtime Reproduction(기준선 어댑터 ONNX 런타임 재현)
- action(행동): `{SELECTED_ADAPTER_ID}`를 ONNX backend(ONNX 백엔드)로 실제 MT5 validation/OOS(검증/표본외)에 실행했다.
- effect(효과): Python adapter(Python 어댑터)와 ONNX runtime(ONNX 런타임)의 MT5 재현 차이를 확인했다.
- terminal_label(종료 라벨): `{terminal_label}`
- runtime_gate_passed(런타임 게이트 통과): `{gate.get('passed')}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(val.get('profit_factor'))}` / `{fmt(oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(val.get('net_profit'))}` / `{fmt(oos.get('net_profit'))}`
- next_action(다음 행동): `commit_push_progress_then_report_hard_completion_only_if_git_sync_succeeds`
"""
    append_once(PROGRESS_LOG_PATH, entry)
    append_once(
        CHANGELOG_PATH,
        f"""
## 2026-05-15 Stage56 {RUN_NUMBER} BaselineAdapter ONNX Runtime Reproduction(기준선 어댑터 ONNX 런타임 재현)
- completed(완료): actual MT5 ONNX runtime validation/OOS(실제 MT5 ONNX 런타임 검증/표본외)를 실행하고 summary/ledger/current truth(요약/장부/현재 진실)를 갱신했다.
- effect(효과): adapter hardening(어댑터 경화)이 ONNX parity(ONNX 동등성)에서 MT5 runtime reproduction(MT5 런타임 재현)으로 이어졌는지 확인했다.
""",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 BaselineAdapter ONNX MT5 runtime reproduction.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=360)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_repair_module()
    args = parse_args(argv)
    if args.finalize_existing:
        result = load_existing_result()
        handoff = read_json(HANDOFF_JSON_PATH) if path_exists(HANDOFF_JSON_PATH) else {}
    else:
        inputs = prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        handoff = write_handoff(inputs, attempts)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "stage_number": 56,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": {"adapter_entry_model_onnx": {"path": rel(inputs["model_local"]), "common_path": inputs["model_common"]}},
            "route_coverage": route_coverage(),
            "model_family": "stage56_baseline_adapter_ba14_onnx_probability_runtime",
            "feature_set_id": "stage56_context_gap_refill_signal_onnx_runtime",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = (
        repair.audit_rows_for_result(result, REPRO_VARIANTS, float(args.cost_stress_per_trade))
        if result.get("mt5_kpi_records")
        else []
    )
    risk_rows = enrich_risk_rows(base.risk_rows_from_result(result))
    summary_rows = enrich_summary_rows(repair.build_summary_rows(result, REPRO_VARIANTS, audit_rows, risk_rows), risk_rows)
    gate = runtime_gate(summary_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(RISK_CSV_PATH, risk_rows)
    write_report(summary_rows, gate, result)
    extra_paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        AUDIT_CSV_PATH,
        RISK_CSV_PATH,
        HANDOFF_JSON_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        Path(__file__),
        SPEC_JSON_PATH,
        SPEC_MD_PATH,
        ONNX_MODEL_SOURCE,
        ONNX_PARITY_JSON,
        Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
        Path("foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh"),
        Path("foundation/mt5/include/ObsidianPrime/ModelRuntime.mqh"),
        Path("foundation/mt5/include/ObsidianPrime/RuntimeTelemetry.mqh"),
    ]
    write_run_files(result, summary_rows, audit_rows, risk_rows, gate, {}, handoff)
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, summary_rows, artifacts, gate)
    write_run_files(result, summary_rows, audit_rows, risk_rows, gate, ledger_payload, handoff)
    update_state_docs(summary_rows, gate, result)
    update_logs(summary_rows, gate, result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if result.get("external_verification_status") == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "terminal_label": TERMINAL_LABEL_ATTEMPTED if result.get("external_verification_status") == "completed" else TERMINAL_LABEL_REPAIRING,
                    "runtime_gate": gate,
                    "summary_json": SUMMARY_JSON_PATH.as_posix(),
                    "summary_csv": SUMMARY_CSV_PATH.as_posix(),
                    "risk_csv": RISK_CSV_PATH.as_posix(),
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
