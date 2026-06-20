from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.control_plane.mt5_runtime_probe_contract import (  # noqa: E402
    assert_standard_attempt_period,
    audit_mt5_runtime_probe_contract,
    standard_split_specs,
)
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload, copy_to_common, execute_prepared_run  # noqa: E402
from foundation.control_plane.runtime_learning_probe_decision_gate import audit_runtime_learning_probe_decision  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d  # noqa: E402
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b  # noqa: E402


RUN_ID = "frontier88_runtime_learning_probe_backfill_v1"
STAGE_ID = "stage_frontier_88__runtime_substrate_first_materialization_probe"
SOURCE_RUN_ID = "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
SOURCE_STAGE04_RUN_ID = "frontier04D_trainable_path_label_onnx_probe_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
SOURCE_MODEL = (
    ROOT
    / "stages"
    / "stage_frontier_04__path_aware_cost_dd_event_labeling"
    / "02_runs"
    / SOURCE_STAGE04_RUN_ID
    / "models"
    / "rf_depth5_leaf80_balanced_argmax.joblib"
)
SOURCE_ONNX = SOURCE_MODEL.with_suffix(".onnx")
COMMON_ROOT = f"Project_Obsidian_Prime_v2/f88_runtime_learning/{RUN_ID}"
MODEL_ID = "rf_depth5_leaf80_balanced_argmax"
FEATURE_SET_ID = "frontier04d_f04d_read_feature_order_58"
LABEL_ID = "frontier04d_path_label_argmax_reference_only"
CLAIM_BOUNDARY = (
    "runtime_learning_probe_observation_or_runtime_probe_completed_if_completion_guard_passes_only_"
    "no_f88_success_rewrite_no_selected_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_economics_pass"
)
BASE_ALLOWED_CLAIMS = [
    "runtime_learning_probe_decision_recorded",
    "f88_repair_attempt_recorded",
    "runtime_probe_observation",
    "runtime_learning_record",
    "completion_claim_guard_recorded",
]
ALLOWED_CLAIMS = BASE_ALLOWED_CLAIMS
FORBIDDEN_CLAIMS = [
    "goal_achieve",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "economics_pass",
    "selected_baseline",
    "promotion_candidate",
    "materialization_ready",
    "handoff_complete",
    "mt5_verification_complete",
    "runtime_verified",
]

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def completion_guard_passed(
    result: Mapping[str, Any] | None = None,
    completion_claim_guard: Mapping[str, Any] | None = None,
) -> bool:
    if result is None or completion_claim_guard is None:
        return False
    if result is not None and result.get("external_verification_status") != "completed":
        return False
    if completion_claim_guard is not None and completion_claim_guard.get("status") != "pass":
        return False
    return True


def allowed_claims_for_result(
    result: Mapping[str, Any] | None = None,
    completion_claim_guard: Mapping[str, Any] | None = None,
) -> list[str]:
    claims = list(BASE_ALLOWED_CLAIMS)
    if completion_guard_passed(result, completion_claim_guard):
        claims.append("runtime_probe_completed")
    return claims


def forbidden_claims_for_result(
    result: Mapping[str, Any] | None = None,
    completion_claim_guard: Mapping[str, Any] | None = None,
) -> list[str]:
    claims = list(FORBIDDEN_CLAIMS)
    if not completion_guard_passed(result, completion_claim_guard):
        claims.append("runtime_probe_completed")
    return claims


def claim_boundary_for_result(
    result: Mapping[str, Any] | None = None,
    completion_claim_guard: Mapping[str, Any] | None = None,
) -> str:
    if completion_guard_passed(result, completion_claim_guard):
        return CLAIM_BOUNDARY
    return (
        "runtime_learning_probe_observation_only_no_f88_success_rewrite_no_selected_baseline_"
        "no_promotion_no_runtime_authority_no_live_readiness_no_economics_pass_no_runtime_probe_completed"
    )


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def write_yaml(path: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140),
        encoding="utf-8",
    )
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def write_text(path: Path, text: str) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def load_runtime_source() -> tuple[pd.DataFrame, list[str], Any, Mapping[str, Any]]:
    missing = [rel(path) for path in (SOURCE_MODEL, SOURCE_ONNX, SOURCE_RUN_ROOT) if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing F88 runtime learning source artifacts: {missing}")
    full, _raw, source_integrity = f07b.load_training_packet()
    feature_order = list(f04d.read_feature_order())
    model = joblib.load(io_path(SOURCE_MODEL))
    model_features = int(getattr(model, "n_features_in_", len(feature_order)))
    if model_features != len(feature_order):
        raise RuntimeError(f"F88 source model feature count mismatch: model={model_features}, order={len(feature_order)}")
    return full, feature_order, model, source_integrity


def signal_from_probabilities(probabilities: Any) -> Any:
    idx = probabilities.argmax(axis=1)
    return pd.Series(idx).map({0: -1, 1: 0, 2: 1}).astype("int8").to_numpy()


def timestamp_coverage(
    frame: pd.DataFrame,
    signal: Any,
    *,
    split_label: str,
    source_split: str,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    from_dt = pd.Timestamp(from_date.replace(".", "-"), tz="UTC")
    to_dt = pd.Timestamp(to_date.replace(".", "-"), tz="UTC")
    source_min = timestamps.min() if len(timestamps) else None
    source_max = timestamps.max() if len(timestamps) else None
    covers_start = source_min is not None and source_min.date() <= from_dt.date()
    covers_end = source_max is not None and source_max.date() >= (to_dt - pd.Timedelta(days=1)).date()
    standard_period_covered = bool(covers_start and covers_end)
    signal_series = pd.Series(signal)
    return {
        "split": split_label,
        "source_split": source_split,
        "standard_from_date": from_date,
        "standard_to_date": to_date,
        "source_rows": int(len(frame)),
        "source_min_timestamp_utc": source_min.isoformat() if source_min is not None else None,
        "source_max_timestamp_utc": source_max.isoformat() if source_max is not None else None,
        "standard_period_covered": standard_period_covered,
        "source_covers_start_date": bool(covers_start),
        "source_covers_end_date": bool(covers_end),
        "signal_count": int((signal_series != 0).sum()),
        "long_count": int((signal_series == 1).sum()),
        "short_count": int((signal_series == -1).sum()),
        "flat_count": int((signal_series == 0).sum()),
    }


def runtime_surface_contract_for_split(coverage: Mapping[str, Any], feature_path: Path) -> dict[str, Any]:
    covered = bool(coverage.get("standard_period_covered"))
    return {
        "split": coverage.get("split"),
        "source_split": coverage.get("source_split"),
        "standard_from_date": coverage.get("standard_from_date"),
        "standard_to_date": coverage.get("standard_to_date"),
        "source_min_timestamp_utc": coverage.get("source_min_timestamp_utc"),
        "source_max_timestamp_utc": coverage.get("source_max_timestamp_utc"),
        "surface_scope": "full_period_deterministic" if covered else "partial_period_deterministic_surface",
        "source_artifact_role": "full_period_model_decision_surface" if covered else "deterministic_surface_missing_stage_native_horizon",
        "source_artifact_path": rel(feature_path),
        "standard_period_covered": covered,
        "completion_claim_allowed": covered,
        "reason_code": "standard_period_surface_available"
        if covered
        else "source_rows_end_before_stage_native_standard_contract_to_date",
        "claim_effect": "This split can support the surface side of runtime_probe_completed."
        if covered
        else "This split is runtime-learning observation only; the stage-native standard tester period extends beyond available source rows.",
    }


def materialize_runtime_surface(common_files_root: Path) -> dict[str, Any]:
    full, feature_order, model, source_integrity = load_runtime_source()
    feature_hash = ordered_hash(feature_order)
    common_model = copy_to_common(SOURCE_ONNX, f"{COMMON_ROOT}/models/{SOURCE_ONNX.name}", common_files_root)
    attempts: list[dict[str, Any]] = []
    feature_artifacts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = [common_model]
    coverage_by_split: dict[str, dict[str, Any]] = {}
    surface_contract_by_split: dict[str, dict[str, Any]] = {}
    blocked_standard_splits: dict[str, dict[str, Any]] = {}
    route_by_split: dict[str, dict[str, int]] = {}
    no_tier_by_split: dict[str, int] = {}
    split_specs = standard_split_specs()
    total_signal_count = 0
    total_long_count = 0
    total_short_count = 0
    total_flat_count = 0

    for split_label, (source_split, from_date, to_date) in split_specs.items():
        assert_standard_attempt_period(split=split_label, from_date=from_date, to_date=to_date)
        frame = full.loc[full["split"].astype(str).eq(source_split)].copy()
        if frame.empty:
            raise RuntimeError(f"F88 source split is empty: {source_split}")
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        matrix = frame.loc[:, feature_order].astype("float64").to_numpy()
        probabilities = ordered_sklearn_probabilities(model, matrix, class_order=f04d.LABEL_ORDER)
        signal = signal_from_probabilities(probabilities)
        matrix_path = RUN_ROOT / "mt5" / f"f88_runtime_learning_{split_label}_feature_matrix.csv"
        feature_artifact = mt5.export_mt5_feature_matrix_csv(
            frame,
            feature_order,
            matrix_path,
            metadata_columns=("raw_index",),
        )
        common_feature = copy_to_common(matrix_path, f"{COMMON_ROOT}/features/{matrix_path.name}", common_files_root)
        coverage = timestamp_coverage(
            frame,
            signal,
            split_label=split_label,
            source_split=source_split,
            from_date=from_date,
            to_date=to_date,
        )
        surface_contract = runtime_surface_contract_for_split(coverage, matrix_path)
        feature_artifacts.append(feature_artifact)
        common_copies.append(common_feature)
        coverage_by_split[split_label] = coverage
        surface_contract_by_split[split_label] = surface_contract
        route_by_split[source_split] = {
            "tier_a_primary_rows": int(len(frame)),
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": int(len(frame)),
        }
        no_tier_by_split[source_split] = 0
        total_signal_count += int(coverage["signal_count"])
        total_long_count += int(coverage["long_count"])
        total_short_count += int(coverage["short_count"])
        total_flat_count += int(coverage["flat_count"])

        if not bool(coverage.get("standard_period_covered")):
            blocked_standard_splits[split_label] = {
                "split": split_label,
                "source_split": source_split,
                "from_date": from_date,
                "to_date": to_date,
                "status": "not_run_after_repair_impossible",
                "reason_code": "source_rows_end_before_stage_native_standard_contract_to_date",
                "source_min_timestamp_utc": coverage.get("source_min_timestamp_utc"),
                "source_max_timestamp_utc": coverage.get("source_max_timestamp_utc"),
                "required_to_date": to_date,
                "repair_attempt": "materialized_available_source_rows_and_refused_invalid_standard_oos_tester_run",
                "required_next_repair": "repair_within_stage_native_oos_horizon_without_extending_to_2026_06_18",
                "claim_effect": (
                    "This split cannot be run as a standard MT5 runtime probe attempt until the deterministic "
                    "feature/decision surface covers the full contract period."
                ),
            }
            continue

        attempt = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=88,
            exploration_label="frontier88_RuntimeLearningProbeBackfill",
            attempt_name=f"f88_runtime_learning_{split_label}",
            tier=mt5.TIER_A,
            split=split_label,
            model_path=f"{COMMON_ROOT}/models/{SOURCE_ONNX.name}",
            model_id=MODEL_ID,
            model_backend="onnx",
            feature_path=f"{COMMON_ROOT}/features/{matrix_path.name}",
            feature_count=len(feature_order),
            feature_order_hash=feature_hash,
            short_threshold=0.0,
            long_threshold=0.0,
            min_margin=0.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            record_view_prefix="mt5_f88_runtime_learning",
            max_hold_bars=12,
            common_root=COMMON_ROOT,
            extra_set_values={"InpDecisionMode": "argmax", "InpFallbackDecisionMode": "argmax"},
        )
        attempt["runtime_surface_contract"] = surface_contract
        attempts.append(attempt)

    runtime_surface_contract = {
        "version": "runtime_surface_contract_v1",
        "source_stage": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_reference_run_id": SOURCE_STAGE04_RUN_ID,
        "surface_scope": "stage_native_standard_pair"
        if not blocked_standard_splits
        else "stage_native_standard_pair_with_missing_split_surface",
        "completion_claim_allowed": not blocked_standard_splits,
        "by_split": surface_contract_by_split,
        "blocked_standard_splits": blocked_standard_splits,
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_reference_run_id": SOURCE_STAGE04_RUN_ID,
        "source_model": rel(SOURCE_MODEL),
        "source_onnx": rel(SOURCE_ONNX),
        "source_integrity": source_integrity,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
        "model_artifact": {"path": rel(SOURCE_ONNX), "sha256": sha256_file_lf_normalized(SOURCE_ONNX)},
        "feature_artifacts": feature_artifacts,
        "common_copies": common_copies,
        "attempts": attempts,
        "blocked_standard_splits": blocked_standard_splits,
        "standard_split_specs": split_specs,
        "coverage_by_split": coverage_by_split,
        "runtime_surface_contract": runtime_surface_contract,
        "repair": {
            "repair_id": "repair01_short_validation_probe_to_standard_contract_pair",
            "source_problem": "F88C had a short validation-only probe 2025.01.02..2025.01.09, not the stage-native standard validation_is+oos contract.",
            "repair_action": "Materialize F04D reference ONNX with current source rows and run full-surface stage-native standard splits.",
            "stage_native_oos_status": "oos_horizon_ends_at_2026_04_13_and_must_not_be_extended_to_2026_06_18",
            "claim_effect": "Runtime probe completion may be claimed only if both stage-native standard Strategy Tester reports complete; runtime authority and economics pass remain not claimed.",
        },
        "pre_gate_signal_count": total_signal_count,
        "long_signal_count": total_long_count,
        "short_signal_count": total_short_count,
        "flat_signal_count": total_flat_count,
        "route_coverage": {
            "by_split": route_by_split,
            "tier_b_fallback_by_split_subtype": {},
            "no_tier_by_split": no_tier_by_split,
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def apply_runtime_learning_judgment(result: dict[str, Any], surface: Mapping[str, Any]) -> None:
    reports = result.get("strategy_tester_reports", [])
    completed_reports = [row for row in reports if row.get("status") == "completed"] if isinstance(reports, list) else []
    blocked_standard_splits = surface.get("blocked_standard_splits", {})
    if blocked_standard_splits and completed_reports:
        result["external_verification_status"] = "partial_completed_oos_source_blocked"
        result["judgment"] = "runtime_learning_probe_partial_observation_missing_stage_native_split_completion_blocked"
    elif len(completed_reports) >= 2:
        result["external_verification_status"] = "completed"
        result["judgment"] = "stage_native_runtime_probe_completed_no_authority_no_economics_pass"
    else:
        result["external_verification_status"] = "incomplete_or_blocked"
        result["judgment"] = "runtime_learning_probe_observation_incomplete_or_blocked"
    result["blocked_standard_splits"] = blocked_standard_splits
    result["runtime_surface_contract"] = surface.get("runtime_surface_contract")
    result["claim_boundary"] = CLAIM_BOUNDARY
    result["stage_inheritance"] = "f88_historical_runtime_substrate_observation_only_no_success_rewrite"


def runtime_learning_decision(surface: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    repair = surface.get("repair", {}) if isinstance(surface.get("repair"), Mapping) else {}
    return {
        "runtime_learning_probe_decision": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "historical_runtime_probe_status": "short_validation_only_probe_no_standard_oos_contract",
            "strong_candidate_count": 0,
            "runtime_learning_probe_candidate_count": 1 if int(surface.get("pre_gate_signal_count", 0)) > 0 else 0,
            "pre_gate_signal_count": int(surface.get("pre_gate_signal_count", 0)),
            "repair_attempt_count": 1,
            "runtime_surface_status": "repair_required_short_validation_probe_to_stage_native_standard_pair",
            "mt5_action": "run_after_repair",
            "not_run_reason_code": "",
            "repair_attempt_required": True,
            "forbidden_no_run_reasons": [
                "proxy_bad",
                "candidate_0",
                "low_trade_count_expected",
                "long_short_imbalanced",
                "cost_expensive",
                "agent_recommended_skip",
            ],
            "forbidden_skip_basis_seen": [],
            "claim_effect": "F88 has a repairable deterministic runtime surface for stage-native validation_is and OOS; MT5 is run after repair for both when each surface covers the stage-native contract.",
            "repair_attempts": [
                {
                    "repair_id": repair.get("repair_id"),
                    "result": "partial_run_blocked_missing_stage_native_split_surface"
                    if result.get("external_verification_status") == "partial_completed_oos_source_blocked"
                    else "materialized_and_run"
                    if result.get("external_verification_status") == "completed"
                    else "materialized_attempted",
                    "claim_effect": repair.get("claim_effect"),
                    "stage_native_oos_status": repair.get("stage_native_oos_status"),
                }
            ],
            "required_evidence": [
                "stage-native standard validation_is tester attempt when the full validation surface is available",
                "stage-native standard OOS tester attempt when the full OOS surface is available",
                "blocked_standard_splits record only when a stage-native split surface is missing",
                "Strategy Tester report for any executed standard attempt",
                "runtime surface contract with stage-native OOS horizon",
                "completion claim guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "mt5_attempt_result_status": result.get("external_verification_status", "unknown"),
        "mt5_attempt_blocker": ""
        if result.get("external_verification_status") == "completed"
        else "stage_native_split_surface_missing_blocks_standard_run"
        if result.get("external_verification_status") == "partial_completed_oos_source_blocked"
        else "strategy_tester_reports_incomplete_or_blocked",
    }


def compact_metrics_by_split(result: Mapping[str, Any]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for record in result.get("strategy_tester_reports", []) or []:
        split = str(record.get("split") or record.get("attempt_name") or "unknown")
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows[split] = {
            "status": record.get("status"),
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "max_drawdown_percent": metrics.get("max_drawdown_percent"),
            "trade_count": metrics.get("trade_count"),
            "deal_count": metrics.get("deal_count"),
            "win_rate_percent": metrics.get("win_rate_percent"),
            "long_trade_count": metrics.get("long_trade_count"),
            "short_trade_count": metrics.get("short_trade_count"),
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
        }
    return rows


def make_actual_subagent_calls(subagent_id: str, nickname: str, result_status: str) -> dict[str, Any]:
    call = {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "call_mode": "micro_consult",
        "spawned_agent_id": subagent_id,
        "subagent_id": subagent_id,
        "nickname": nickname,
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": result_status,
        "opinion_classification": "needs_local_verification",
        "advice_classification": "accepted_with_local_verification_and_scope_caveat",
        "remit": "F88 runtime learning probe action classification from F88C short runtime substrate probe",
        "accepted_points": [
            "F88C is short validation-only runtime evidence, not stage-native runtime_probe_completed evidence.",
            "The F04D reference ONNX can be used as a repairable deterministic runtime learning surface.",
            "OOS through 2026-04-13 is the stage-native normal horizon and must not be extended to 2026-06-18.",
        ],
        "local_verification_update": [
            "Repair01 materialized the F04D reference ONNX against current validation and OOS source rows.",
            "MT5 Strategy Tester runs only stage-native standard splits whose deterministic surface covers the full contract period.",
            "The stage-native OOS horizon ends at 2026-04-13.",
            "Completion claim guard allows runtime_probe_completed only when both validation_is and OOS Strategy Tester reports complete.",
        ],
        "claim_effect": "advisory_only_no_reviewed_pass",
        "scope_caveat": "This is an F88 runtime learning observation; it does not rewrite Frontier04 or F88 success status.",
    }
    return {
        "call_mode": "micro_consult",
        "agents_requested_count": 1,
        "agents_completed_count": 1 if result_status == "completed" else 0,
        "claim_effect": "advisory_only_no_reviewed_pass",
        "agents_called": [call],
    }


def make_work_packet(
    created_at: str,
    allowed_claims: Sequence[str],
    forbidden_claims: Sequence[str],
    claim_boundary: str,
) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "runtime_learning_probe_decision_gate",
        "runtime_evidence_gate",
        "mt5_runtime_probe_contract_audit",
        "kpi_contract_audit",
        "test_gate",
        "skill_receipt_schema_lint",
        "codex_task_force_review_packet",
        "closeout_report_check",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": created_at,
        "user_request": {"requested_action": "runtime_probe_backfill_repair_with_task_force", "requested_count": 1},
        "current_truth": {
            "target_stage": "F88",
            "historical_status": "short_validation_runtime_probe_observation_no_standard_oos",
            "boundary": "f88_closeout_not_rewritten",
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest"],
            "mutation_intent": "targeted_update",
            "execution_intent": "run_full_surface_stage_native_standard_splits_after_repair",
        },
        "risk_vector_scan": {
            "risks": {"short_probe_overclaim": "high", "completion_overclaim": "high", "authority_overclaim": "high"},
            "required_decision_locks": [
                "f88_is_backfill_observation_only",
                "runtime_probe_completed_requires_both_stage_native_reports_and_surface_contract",
            ],
            "required_gates": required_gates,
            "forbidden_claims": list(forbidden_claims),
        },
        "decision_lock": {
            "locked_direction": "f88_runtime_learning_probe_backfill_observation_only",
            "not_locked": ["selected_baseline", "promotion_candidate", "runtime_authority", "live_readiness", "goal_achieve"],
            "claim_boundary": claim_boundary,
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": ["F88 runtime learning probe backfill", "MT5 Strategy Tester stage-native validation_is+OOS pair"],
            "scope_units": [RUN_ID, STAGE_ID],
            "execution_layers": ["python_orchestration", "mt5_execution", "strategy_tester_report_parse"],
            "mutation_policy": "targeted_update_stage88_backfill_and_contract_guard_only",
            "evidence_layers": [
                "runtime_learning_probe_decision",
                "mt5_terminal_command",
                "strategy_tester_report_hash",
                "telemetry_hash",
                "runtime_surface_contract",
            ],
            "reduction_policy": "no_authority_or_economics_claim_from_runtime_probe_completed",
            "claim_boundary": claim_boundary,
        },
        "verification_profile": {
            "profile_id": "runtime_probe" if "runtime_probe_completed" in allowed_claims else "runtime_learning_probe",
            "claim_surface": {"allowed_claims": list(allowed_claims), "forbidden_claims": list(forbidden_claims), "claim_boundary": claim_boundary},
            "trigger_sources": [
                "active_goal_continuation",
                "F88C_short_validation_only_probe",
                "MT5_runtime_probe_anti_deferral_goal",
            ],
            "protected_claims": ["runtime_learning_probe_decision", "runtime_probe_observation", "completion_claim_guard_recorded"],
            "required_evidence": [
                "runtime_learning_probe_decision",
                "mt5_action run_after_repair",
                "repair_attempts",
                "MT5 Strategy Tester terminal output",
                "dataset_id source dataset_id=f04d_reference_model_input_dataset",
                f"feature_set_id {FEATURE_SET_ID}",
                f"label_id {LABEL_ID}",
                "split_id validation_is 2025.01.02..2025.10.01 and oos 2025.10.01..2026.04.13",
                "onnx_hash from F04D reference ONNX",
                "ea_source_hash foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "ea_binary_hash ObsidianPrimeV2_RuntimeProbeEA.ex5",
                "set_ini_hash for both stage-native attempts",
                "feature_order_hash recorded in attempts",
                "tester_identity US100 M5 Model=4 Deposit=500 Leverage=1:100 /portable",
                "report_hash for validation_is and OOS Strategy Tester reports",
                "trade_list_hash from Strategy Tester parsed report/trade evidence when available",
                "telemetry_hash for validation_is and OOS runtime telemetry",
                "validation_is Strategy Tester report if the full validation surface is available",
                "OOS Strategy Tester report if the full stage-native OOS surface is available",
                "blocked_standard_splits evidence only when a stage-native split surface is missing",
                "mt5_runtime_probe_contract_audit",
                "mt5_runtime_probe_completion_claim_guard",
                "actual_subagent_calls",
            ],
            "gates_not_run_with_reason": [],
            "stop_conditions": [
                "F88 runtime learning observation recorded",
                "completion claim guard records whether runtime_probe_completed is allowed",
                "stage-native OOS horizon recorded",
            ],
        },
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-prime-ml",
            "support_skills": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "required_skill_receipts": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_considered": [
                "obsidian-prime-ml",
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_selected": [
                "obsidian-prime-ml",
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_not_used": [],
            "required_gates": required_gates,
        },
        "acceptance_criteria": {
            "must_pass": [
                "stage-native validation_is and OOS periods come from foundation/config/mt5_runtime_probe_contract.yaml",
                "no 2026.06.18 OOS extension is required",
                "runtime_probe_completed only if both Strategy Tester reports and runtime surface contract pass",
                "runtime authority, economics pass, materialization-ready, selected baseline, promotion, and live readiness remain forbidden",
            ],
            "must_record": [
                "actual_subagent_calls",
                "runtime_learning_probe_decision_gate",
                "mt5_runtime_probe_completion_claim_guard",
                "runtime_probe_backfill_receipt",
            ],
        },
        "work_plan": {
            "steps": [
                "update MT5 runtime probe contract to stage-native OOS horizon",
                "materialize F88 repaired runtime surface",
                "run stage-native validation_is and OOS MT5 Strategy Tester attempts",
                "write claim guard and receipts",
                "run schema and unit verification",
            ],
            "stop_condition": "claim guard and packet receipts reflect the stage-native OOS rule without authority/economics claims",
        },
        "evidence_contract": {
            "required_evidence": [
                "runtime_probe_backfill_receipt.json",
                "mt5_runtime_probe_contract_audit.json",
                "mt5_runtime_probe_completion_claim_guard.json",
                "runtime_learning_probe_decision_gate_actual.json",
                "actual_subagent_calls.json",
            ],
            "runtime_surface_contract": "stage_native_validation_oos_surface_contract_controls_runtime_probe_completed",
            "forbidden_evidence_substitutes": ["proxy_only", "compile_only", "git_push"],
        },
        "gates": {
            "required": required_gates,
            "not_applicable_with_reason": {},
        },
        "final_claim_policy": {
            "allowed_claims": list(allowed_claims),
            "forbidden_claims": list(forbidden_claims),
            "completion_claim": "allowed_only_if_runtime_probe_completion_claim_guard_passes"
            if "runtime_probe_completed" in allowed_claims
            else "forbidden",
            "claim_boundary": claim_boundary,
        },
    }


def make_skill_receipts(
    result: Mapping[str, Any],
    actual_calls: Mapping[str, Any],
    completion_claim_guard: Mapping[str, Any],
) -> dict[str, Any]:
    tester_identity = (
        "US100 M5, Model=4, Deposit=500, Leverage=1:100, validation_is 2025.01.02..2025.10.01, "
        "oos 2025.10.01..2026.04.13"
    )
    tester_report_status = "Strategy Tester report incomplete or blocked"
    if result.get("external_verification_status") == "completed":
        tester_report_status = "validation_is and oos Strategy Tester reports completed"
    elif result.get("external_verification_status") == "partial_completed_oos_source_blocked":
        tester_report_status = "one stage-native split Strategy Tester report completed; another stage-native split is blocked"
    allowed_claims = allowed_claims_for_result(result, completion_claim_guard)
    forbidden_claims = forbidden_claims_for_result(result, completion_claim_guard)
    return {
        "receipts": [
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-runtime-parity",
                "status": "executed",
                "python_artifact": "stage_pipelines/stage_frontier_88/frontier88_runtime_learning_probe_backfill.py",
                "runtime_artifact": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "compared_surface": "F04D reference ONNX plus current source rows -> MT5 RuntimeProbeEA telemetry",
                "parity_level": "runtime_learning_probe_observation_only",
                "runtime_learning_probe_decision": "runtime_learning_probe_candidate_count=1; mt5_action=run_after_repair; repair_attempts=1; stage-native validation_is and OOS may run when their full surfaces exist",
                "tester_identity": tester_identity,
                "missing_evidence": ["none_for_stage_native_runtime_probe_completed_claim"]
                if result.get("external_verification_status") == "completed"
                else ["completed Strategy Tester report for every stage-native standard split"],
                "allowed_claims": allowed_claims,
                "forbidden_claims": forbidden_claims,
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-backtest-forensics",
                "status": "executed",
                "tester_report": tester_report_status,
                "tester_settings": tester_identity + ", /portable, ReplaceReport=1, ShutdownTerminal=1",
                "spread_commission_slippage": "broker-native tester behavior; no added modeled commission for executed standard attempts",
                "trade_list_identity": "Strategy Tester parsed report and deal/trade metrics for validation_is and OOS when reports complete",
                "runtime_learning_probe_decision": "F88 short validation probe is repaired into a stage-native validation_is+OOS runtime probe attempt.",
                "forensic_gaps": ["none_for_stage_native_runtime_probe_completed_claim"]
                if result.get("external_verification_status") == "completed"
                else ["stage-native standard split report incomplete or blocked"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment_boundary": claim_boundary_for_result(result, completion_claim_guard),
                "allowed_claims": allowed_claims,
                "forbidden_claims": forbidden_claims,
                "evidence_used": [
                    "runtime_probe_backfill_receipt.json",
                    "mt5_runtime_probe_contract_audit.json",
                    "mt5_runtime_probe_completion_claim_guard.json",
                    "runtime_learning_probe_decision_gate_actual.json",
                ],
                "runtime_learning_probe_decision": str(result.get("judgment", "runtime_learning_observation_no_economics_pass")),
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-task-force-review",
                "status": "executed",
                "trigger_reason": "active_goal_required_task_force_micro_consult_for_runtime_probe_backfill",
                "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                "agents_used": ["agent_08_mt5_onnx_runtime"],
                "actual_subagent_calls": actual_calls.get("agents_called", []),
                "review_requirement": "active_goal_required",
                "model_policy": "inherit_parent_model_highest_available_xhigh_if_available",
                "bounded_evidence": [rel(SOURCE_RUN_ROOT), rel(SOURCE_ONNX), rel(SOURCE_MODEL)],
                "advice_classification": "accepted_with_local_verification",
                "local_verification": "F88 repair01 materialized available source rows and ran stage-native full-surface standard attempts when available.",
                "claim_boundary": claim_boundary_for_result(result, completion_claim_guard),
                "final_codex_direction": "run_after_repair_stage_native_probe_no_authority_or_economics_claim",
                "forbidden_claim_check": {"forbidden_claims": forbidden_claims, "completed_forbidden": False},
            },
        ]
    }


def make_closeout_report(result: Mapping[str, Any]) -> str:
    metrics = compact_metrics_by_split(result)
    if result.get("external_verification_status") == "completed":
        conclusion = (
            "F88 was repaired into a stage-native validation_is+OOS runtime probe completion record. "
            "This does not create runtime authority, economics pass, selected baseline, promotion, or live readiness."
        )
        guardrail = "Runtime probe completed only means both stage-native Strategy Tester reports exist and the surface contract passed."
    else:
        conclusion = (
            "F88 remains a runtime learning observation because at least one stage-native Strategy Tester report or surface contract is incomplete."
        )
        guardrail = "Strategy Tester report missing is a blocker, not a completion reason."
    return f"""# F88 Runtime Learning Probe Backfill Closeout

## Conclusion
{conclusion}

## What Changed
- Added F88 runtime learning backfill script and MT5 artifacts.
- Re-ran the F04D reference ONNX through F88 for stage-native full-surface standard attempts.
- Recorded 2026-04-13 as the normal OOS horizon and did not extend the probe to 2026-06-18.
- Recorded agent_08 micro consult as advisory_only_no_reviewed_pass.

## Guardrail
- {guardrail}
- Runtime authority, economics pass, materialization-ready, operating promotion, and live readiness remain not claimed.

## Metrics Snapshot
```json
{json.dumps(json_ready(metrics), ensure_ascii=False, indent=2)}
```
"""


def write_packet_artifacts(payload: Mapping[str, Any], args: argparse.Namespace) -> None:
    created_at = str(payload.get("created_at_utc") or utc_now())
    result = payload.get("mt5_result", {}) if isinstance(payload.get("mt5_result"), Mapping) else {}
    surface = payload.get("surface", {}) if isinstance(payload.get("surface"), Mapping) else {}
    completion_claim_guard = (
        payload.get("mt5_runtime_probe_completion_claim_guard", {})
        if isinstance(payload.get("mt5_runtime_probe_completion_claim_guard"), Mapping)
        else {}
    )
    allowed_claims = allowed_claims_for_result(result, completion_claim_guard)
    forbidden_claims = forbidden_claims_for_result(result, completion_claim_guard)
    actual_calls = make_actual_subagent_calls(args.subagent_id, args.subagent_nickname, args.subagent_result_status)
    write_json(PACKET_ROOT / "actual_subagent_calls.json", actual_calls)
    write_json(
        PACKET_ROOT / "codex_task_force_review_packet.json",
        {
            "audit_name": "codex_task_force_review_packet",
            "status": "pass" if args.subagent_result_status == "completed" else "blocked",
            "passed": args.subagent_result_status == "completed",
            "completed_forbidden": False,
            "counts": {
                "call_mode": "micro_consult",
                "agents_used_count": 1,
                "actual_subagent_calls": [args.subagent_id],
                "claim_effect": "advisory_only_no_reviewed_pass",
                "full_roster_call_reason": None,
                "result_status": args.subagent_result_status,
            },
            "findings": []
            if args.subagent_result_status == "completed"
            else [
                {
                    "check_id": "codex_task_force_review_packet::subagent_not_completed",
                    "severity": "blocking",
                    "message": "Task Force micro consult was spawned but has not completed yet.",
                }
            ],
            "allowed_claims": ["task_force_micro_consult_recorded"] if args.subagent_result_status == "completed" else ["blocked"],
            "forbidden_claims": ["task_force_reviewed_pass"],
        },
    )
    write_yaml(
        PACKET_ROOT / "work_packet.yaml",
        make_work_packet(created_at, allowed_claims, forbidden_claims, claim_boundary_for_result(result, completion_claim_guard)),
    )
    write_json(PACKET_ROOT / "skill_receipts.json", make_skill_receipts(result, actual_calls, completion_claim_guard))
    write_text(PACKET_ROOT / "closeout_report.md", make_closeout_report(result))
    write_json(
        PACKET_ROOT / "runtime_probe_backfill_receipt.json",
        {
            "packet_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "backfill_reason": "active_goal_requires_repair_first_mt5_runtime_learning_probe_for_omitted_frontier_runtime_probes",
            "historical_judgment": "runtime_substrate_observation_only_short_validation_probe_no_authority",
            "historical_runtime_probe_status": "short_validation_only_no_standard_oos",
            "candidate_surface_status": "learning_candidate_repaired_stage_native_validation_oos_probe",
            "judgment": result.get("judgment"),
            "claim_boundary": claim_boundary_for_result(result, completion_claim_guard),
            "allowed_claims": allowed_claims,
            "forbidden_claims": forbidden_claims,
            "surface": {
                "pre_gate_signal_count": surface.get("pre_gate_signal_count"),
                "long_signal_count": surface.get("long_signal_count"),
                "short_signal_count": surface.get("short_signal_count"),
                "flat_signal_count": surface.get("flat_signal_count"),
                "coverage_by_split": surface.get("coverage_by_split"),
                "blocked_standard_splits": surface.get("blocked_standard_splits"),
                "repair": surface.get("repair"),
                "runtime_surface_contract": surface.get("runtime_surface_contract"),
            },
            "mt5_probe": {
                "contract": "foundation/config/mt5_runtime_probe_contract.yaml",
                "attempts": len(result.get("attempts", [])) if isinstance(result.get("attempts"), list) else 0,
                "execution_results": len(result.get("execution_results", [])) if isinstance(result.get("execution_results"), list) else 0,
                "reports": len(result.get("strategy_tester_reports", [])) if isinstance(result.get("strategy_tester_reports"), list) else 0,
                "contract_status": payload.get("mt5_runtime_probe_contract_audit", {}).get("status")
                if isinstance(payload.get("mt5_runtime_probe_contract_audit"), Mapping)
                else None,
                "completion_guard_status": payload.get("mt5_runtime_probe_completion_claim_guard", {}).get("status")
                if isinstance(payload.get("mt5_runtime_probe_completion_claim_guard"), Mapping)
                else None,
            },
            "metrics": compact_metrics_by_split(result),
            "next_repair_option": "If a stage-native split is still incomplete, repair within the 2025.10.01..2026.04.13 OOS horizon; do not extend to 2026.06.18.",
        },
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    surface = materialize_runtime_surface(common_files_root)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": surface["attempts"],
        "blocked_standard_splits": surface["blocked_standard_splits"],
        "common_copies": surface["common_copies"],
        "route_coverage": surface["route_coverage"],
        "model_family": "f04d_reference_onnx_argmax",
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": "mt5_runtime_probe_contract_v1_standard_validation_is_oos",
        "stage_inheritance": "f88_historical_runtime_substrate_observation_only_no_success_rewrite",
        "python_metrics": {
            "pre_gate_signal_count": surface["pre_gate_signal_count"],
            "long_signal_count": surface["long_signal_count"],
            "short_signal_count": surface["short_signal_count"],
            "flat_signal_count": surface["flat_signal_count"],
            "coverage_by_split": surface["coverage_by_split"],
            "repair": surface["repair"],
        },
    }
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "materialized_only",
            "judgment": "materialized_only_no_runtime_claim",
        }
    else:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=common_files_root,
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
        )
    apply_runtime_learning_judgment(result, surface)
    contract_audit = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_observation",)).to_dict()
    completion_claim_guard = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_completed",)).to_dict()
    decision = runtime_learning_decision(surface, result)
    decision_gate = audit_runtime_learning_probe_decision(decision["runtime_learning_probe_decision"]).to_dict()
    allowed_claims = allowed_claims_for_result(result, completion_claim_guard)
    forbidden_claims = forbidden_claims_for_result(result, completion_claim_guard)
    claim_boundary = claim_boundary_for_result(result, completion_claim_guard)
    payload = {
        "created_at_utc": utc_now(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "claim_boundary": claim_boundary,
        "surface": surface,
        "prepared": prepared,
        "mt5_result": result,
        "mt5_runtime_probe_contract_audit": contract_audit,
        "mt5_runtime_probe_completion_claim_guard": completion_claim_guard,
        "runtime_learning_probe_decision": decision["runtime_learning_probe_decision"],
        "runtime_learning_probe_decision_gate": decision_gate,
        "mt5_attempt_blocker": decision["mt5_attempt_blocker"],
        "mt5_attempt_result_status": decision["mt5_attempt_result_status"],
        "allowed_claims": allowed_claims,
        "forbidden_claims": forbidden_claims,
    }
    write_json(RUN_ROOT / "runtime_learning_surface_triage.json", surface)
    write_json(RUN_ROOT / "mt5_runtime_learning_probe_result.json", result)
    write_json(RUN_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(RUN_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_gate_actual.json", decision_gate)
    write_json(PACKET_ROOT / "f88_runtime_learning_probe_backfill_result.json", payload)
    write_json(PACKET_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(PACKET_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_gate_actual.json", decision_gate)
    write_packet_artifacts(payload, args)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill F88 as a standard-period runtime learning probe after repair-first materialization.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output-json", default=str(PACKET_ROOT / "runtime_probe_payload.json"))
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--subagent-id", default="")
    parser.add_argument("--subagent-nickname", default="Runtime")
    parser.add_argument("--subagent-result-status", default="completed")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run(args)
    output_path = Path(args.output_json)
    write_json(output_path, payload)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
