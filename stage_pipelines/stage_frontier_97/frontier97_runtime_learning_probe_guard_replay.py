from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.control_plane.mt5_runtime_probe_contract import (  # noqa: E402
    assert_standard_attempt_period,
    audit_mt5_runtime_probe_contract,
    standard_split_specs,
)
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload, copy_to_common, execute_prepared_run  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402


RUN_ID = "frontier97_control_plane_runtime_learning_probe_guard_replay_v1"
STAGE_ID = "stage_frontier_97__first_hit_survival_hazard_event_sparse_axis"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / "frontier97B" / "proxy_scout"
SOURCE_SCORE_SAMPLE = SOURCE_ROOT / "score_sample.csv"
SOURCE_SUMMARY = STAGE_ROOT / "02_runs" / "frontier97B" / "summary.json"
SOURCE_RUNTIME_TRIGGER = SOURCE_ROOT / "runtime_trigger_check.json"
BEST_VARIANT = "extra_trees_first_hit_regime_q90"
SIGNAL_COLUMN = "f97_runtime_learning_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = f"Project_Obsidian_Prime_v2/f97_runtime_learning/{RUN_ID}"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def f97_signal_frame() -> pd.DataFrame:
    if not path_exists(SOURCE_SCORE_SAMPLE):
        raise FileNotFoundError(SOURCE_SCORE_SAMPLE)
    raw = pd.read_csv(io_path(SOURCE_SCORE_SAMPLE))
    frame = raw.loc[raw["variant_id"].astype(str).eq(BEST_VARIANT)].copy()
    if frame.empty:
        raise RuntimeError(f"no rows for {BEST_VARIANT}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["split"] = frame["split"].astype(str).replace({"validation": "validation"})
    side = pd.to_numeric(frame["side"], errors="coerce").fillna(0).clip(-1, 1).astype("int8")
    frame[SIGNAL_COLUMN] = side
    frame["tier_label"] = mt5.TIER_A
    frame["routing_source"] = "f97_score_sample_best_diagnostic_variant"
    frame["entry_decision"] = side.map({1: "long", -1: "short", 0: "flat"}).astype(str)
    return frame.sort_values("timestamp").reset_index(drop=True)


def materialize_runtime_surface(common_files_root: Path) -> dict[str, Any]:
    frame = f97_signal_frame()
    model_path = RUN_ROOT / "models" / "f97_runtime_learning_signal_score_table.csv"
    model_artifact = export_single_discrete_signal_score_table(model_path, feature_order=FEATURE_ORDER)
    common_model = copy_to_common(model_path, f"{COMMON_ROOT}/models/{model_path.name}", common_files_root)
    attempts: list[dict[str, Any]] = []
    feature_artifacts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = [common_model]
    route_by_split: dict[str, dict[str, int]] = {}
    no_tier_by_split: dict[str, int] = {}
    sample_coverage_by_split: dict[str, dict[str, Any]] = {}
    split_specs = standard_split_specs()
    for split_label, (source_split, from_date, to_date) in split_specs.items():
        assert_standard_attempt_period(split=split_label, from_date=from_date, to_date=to_date)
        split_frame = frame.loc[frame["split"].astype(str).eq(source_split)].copy()
        if split_frame.empty:
            raise RuntimeError(f"F97 runtime learning surface has no rows for source split: {source_split}")
        matrix_path = RUN_ROOT / "mt5" / f"f97_runtime_learning_{split_label}_signal_matrix.csv"
        feature_artifact = mt5.export_mt5_feature_matrix_csv(
            split_frame,
            FEATURE_ORDER,
            matrix_path,
            metadata_columns=("variant_id", "source_tier", "route_role", "regime_key", "entry_decision"),
        )
        common_feature = copy_to_common(matrix_path, f"{COMMON_ROOT}/features/{matrix_path.name}", common_files_root)
        feature_artifacts.append(feature_artifact)
        common_copies.append(common_feature)
        attempts.append(
            attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=97,
                exploration_label="frontier97_RuntimeLearningProbeGuardReplay",
                attempt_name=f"f97_runtime_learning_{split_label}",
                tier=mt5.TIER_A,
                split=split_label,
                model_path=f"{COMMON_ROOT}/models/{model_path.name}",
                model_id=f"{RUN_ID}_single_signal_table",
                model_backend="ebm_table",
                feature_path=f"{COMMON_ROOT}/features/{matrix_path.name}",
                feature_count=len(FEATURE_ORDER),
                feature_order_hash=ordered_hash(FEATURE_ORDER),
                short_threshold=0.55,
                long_threshold=0.55,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_f97_runtime_learning",
                max_hold_bars=12,
                common_root=COMMON_ROOT,
            )
        )
        route_by_split[source_split] = {
            "tier_a_primary_rows": int(len(split_frame)),
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": int(len(split_frame)),
        }
        no_tier_by_split[source_split] = 0
        timestamps = pd.to_datetime(split_frame["timestamp"], utc=True)
        sample_coverage_by_split[split_label] = {
            "source_split": source_split,
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "sample_rows": int(len(split_frame)),
            "sample_min_timestamp_utc": timestamps.min().isoformat(),
            "sample_max_timestamp_utc": timestamps.max().isoformat(),
            "claim_effect": "standard_tester_period_with_sparse_source_sample_no_completion_without_report",
        }
        attempts[-1]["runtime_surface_contract"] = {
            "split": split_label,
            "source_split": source_split,
            "surface_scope": "sparse_diagnostic_sample",
            "source_artifact_role": "score_sample",
            "source_artifact_path": rel(SOURCE_SCORE_SAMPLE),
            "source_min_timestamp_utc": sample_coverage_by_split[split_label]["sample_min_timestamp_utc"],
            "source_max_timestamp_utc": sample_coverage_by_split[split_label]["sample_max_timestamp_utc"],
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "completion_claim_allowed": False,
            "standard_period_covered": False,
            "reason_code": "score_sample_is_not_full_runtime_surface",
            "claim_effect": "MT5 tester observation is allowed, but runtime_probe_completed is blocked until a full-period deterministic or full-period sparse decision surface is materialized.",
        }
    split_rows = int(len(frame))
    long_rows = int(frame[SIGNAL_COLUMN].eq(1).sum())
    short_rows = int(frame[SIGNAL_COLUMN].eq(-1).sum())
    route_coverage = {
        "by_split": route_by_split,
        "tier_b_fallback_by_split_subtype": {},
        "no_tier_by_split": no_tier_by_split,
    }
    runtime_surface_contract = {
        "surface_scope": "sparse_diagnostic_sample",
        "source_artifact_role": "score_sample",
        "source_artifact_path": rel(SOURCE_SCORE_SAMPLE),
        "completion_claim_allowed": False,
        "standard_period_covered": False,
        "reason_code": "score_sample_is_not_full_runtime_surface",
        "by_split": {
            attempt["split"]: attempt["runtime_surface_contract"]
            for attempt in attempts
            if isinstance(attempt.get("runtime_surface_contract"), Mapping)
        },
        "claim_effect": "runtime_learning_observation_only_no_runtime_probe_completed_claim",
    }
    return {
        "source_score_sample": rel(SOURCE_SCORE_SAMPLE),
        "source_summary": rel(SOURCE_SUMMARY),
        "source_runtime_trigger": rel(SOURCE_RUNTIME_TRIGGER),
        "best_variant": BEST_VARIANT,
        "signal_column": SIGNAL_COLUMN,
        "feature_order_hash": ordered_hash(FEATURE_ORDER),
        "pre_gate_signal_count": split_rows,
        "long_signal_count": long_rows,
        "short_signal_count": short_rows,
        "standard_split_specs": split_specs,
        "sample_coverage_by_split": sample_coverage_by_split,
        "runtime_surface_contract": runtime_surface_contract,
        "model_artifact": model_artifact,
        "feature_artifacts": feature_artifacts,
        "common_copies": common_copies,
        "attempts": attempts,
        "route_coverage": route_coverage,
        "claim_effect": "runtime_learning_probe_surface_only_standard_attempts_required_before_completion_claim",
    }


def selected_mt5_blocker(result: Mapping[str, Any]) -> str:
    compile_payload = result.get("compile", {}) if isinstance(result.get("compile"), Mapping) else {}
    if compile_payload.get("status") != "completed":
        return str(compile_payload.get("blocker") or "compile_blocked")
    for row in result.get("execution_results", []) if isinstance(result.get("execution_results"), list) else []:
        if isinstance(row, Mapping) and row.get("status") != "completed":
            return str(row.get("blocker") or row.get("runtime_outputs", {}).get("wait_status") or "tester_blocked")
    if result.get("external_verification_status") != "completed":
        return "runtime_outputs_or_report_blocked"
    return ""


def runtime_learning_decision(surface: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    blocker = selected_mt5_blocker(result)
    mt5_action = "run_probe"
    not_run_reason_code = ""
    if blocker in {"metaeditor_missing", "terminal_missing"}:
        not_run_reason_code = "mt5_environment_blocked_after_attempt"
    return {
        "runtime_learning_probe_decision": {
            "pre_gate_signal_count": int(surface.get("pre_gate_signal_count", 0)),
            "strong_candidate_count": 0,
            "runtime_learning_probe_candidate_count": 1 if int(surface.get("pre_gate_signal_count", 0)) > 0 else 0,
            "runtime_surface_status": "probe_candidate_available",
            "mt5_action": mt5_action,
            "not_run_reason_code": not_run_reason_code,
            "repair_attempt_required": True,
            "repair_attempts": [
                {
                    "attempt_id": "repair01_f97_score_sample_to_standard_validation_oos_runtime_surface",
                    "action": "repackaged F97 score_sample side column into standard validation_is plus oos MT5 runtime learning attempts",
                    "result": "materialized",
                    "model_artifact": surface.get("model_artifact", {}),
                    "feature_artifacts": surface.get("feature_artifacts", []),
                }
            ],
            "forbidden_skip_basis_seen": [],
            "claim_effect": "runtime_learning_probe_decision_only_no_runtime_authority_no_economics_pass",
        },
        "mt5_attempt_blocker": blocker,
        "mt5_attempt_result_status": result.get("external_verification_status", "blocked"),
    }


def apply_f97_runtime_learning_judgment(result: dict[str, Any]) -> None:
    result["claim_boundary"] = (
        "runtime_learning_probe_observation_only_no_f97_success_rewrite_no_baseline_no_promotion_"
        "no_runtime_authority_no_live_readiness_no_economics_pass"
    )
    if result.get("external_verification_status") != "completed":
        result["judgment"] = "blocked_runtime_learning_probe_observation_no_runtime_completion"
        return
    records = result.get("mt5_kpi_records", [])
    metrics = [record.get("metrics", {}) for record in records if isinstance(record, Mapping)]
    if metrics and all(float(row.get("net_profit") or 0.0) <= 0.0 or float(row.get("profit_factor") or 0.0) < 1.0 for row in metrics):
        result["judgment"] = "negative_runtime_learning_probe_observation_completed_no_economics_pass"
        return
    result["judgment"] = "inconclusive_runtime_learning_probe_observation_completed_no_economics_pass"


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    surface = materialize_runtime_surface(common_files_root)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": "frontier97B_first_hit_survival_hazard_event_sparse_proxy_scout_v1",
        "run_root": RUN_ROOT,
        "attempts": surface["attempts"],
        "common_copies": surface["common_copies"],
        "route_coverage": surface["route_coverage"],
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "f97_score_sample_side_signal_runtime_learning_surface",
        "label_id": "f97_first_hit_survival_hazard_event_sparse_proxy_side",
        "split_contract": "mt5_runtime_probe_contract_v1_standard_validation_is_oos",
        "stage_inheritance": "f97_historical_negative_memory_only_no_success_rewrite",
        "python_metrics": {
            "pre_gate_signal_count": surface["pre_gate_signal_count"],
            "long_signal_count": surface["long_signal_count"],
            "short_signal_count": surface["short_signal_count"],
            "sample_coverage_by_split": surface["sample_coverage_by_split"],
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
    apply_f97_runtime_learning_judgment(result)
    contract_audit = audit_mt5_runtime_probe_contract(
        result,
        requested_claims=("runtime_probe_observation",),
    ).to_dict()
    completion_claim_guard = audit_mt5_runtime_probe_contract(
        result,
        requested_claims=("runtime_probe_completed",),
    ).to_dict()
    decision = runtime_learning_decision(surface, result)
    payload = {
        "created_at_utc": utc_now(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "claim_boundary": "runtime_learning_probe_replay_only_no_f97_success_rewrite_no_runtime_authority",
        "surface": surface,
        "prepared": prepared,
        "mt5_result": result,
        "mt5_runtime_probe_contract_audit": contract_audit,
        "mt5_runtime_probe_completion_claim_guard": completion_claim_guard,
        "runtime_learning_probe_decision": decision["runtime_learning_probe_decision"],
        "mt5_attempt_blocker": decision["mt5_attempt_blocker"],
        "mt5_attempt_result_status": decision["mt5_attempt_result_status"],
        "forbidden_claims": [
            "goal_achieve",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "economics_pass",
            "materialization_ready",
            "handoff_complete",
        ],
    }
    write_json(RUN_ROOT / "runtime_learning_surface_triage.json", surface)
    write_json(RUN_ROOT / "mt5_runtime_learning_probe_result.json", result)
    write_json(RUN_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(RUN_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(PACKET_ROOT / "f97_runtime_learning_probe_guard_replay_result.json", payload)
    write_json(PACKET_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(PACKET_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay F97 as a runtime learning probe guard fixture.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--output-json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run(args)
    if args.output_json:
        write_json(Path(args.output_json), payload)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0 if payload.get("mt5_attempt_result_status") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
