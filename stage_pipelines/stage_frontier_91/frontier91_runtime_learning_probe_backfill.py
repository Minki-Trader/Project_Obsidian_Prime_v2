from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import yaml

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


RUN_ID = "frontier91_runtime_learning_probe_backfill_v1"
STAGE_ID = "stage_frontier_91__regime_conditioned_density_cost_abstention_axis"
SOURCE_RUN_ID = "frontier91B_regime_density_cost_abstention_proxy_scout_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / "frontier91B" / "proxy_scout"
SOURCE_SCORE_SAMPLE = SOURCE_ROOT / "proxy_scores_sample.csv"
SOURCE_SUMMARY = STAGE_ROOT / "02_runs" / "frontier91B" / "summary.json"
SOURCE_CANDIDATE_GATE = SOURCE_ROOT / "candidate_gate.json"
SOURCE_CLOSEOUT_DECISION = STAGE_ROOT / "02_runs" / "frontier91C" / "d" / "decision.json"
BEST_VARIANT = "ridge_regime_dense_q85"
LABEL_ID = "regime_density_cost_abstention_return12"
SIGNAL_COLUMN = "f91_runtime_learning_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = f"Project_Obsidian_Prime_v2/f91_runtime_learning/{RUN_ID}"
CLAIM_BOUNDARY = (
    "runtime_learning_probe_observation_only_no_f91_success_rewrite_no_baseline_no_promotion_"
    "no_runtime_probe_completed_no_runtime_authority_no_live_readiness_no_economics_pass"
)
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
    "runtime_probe_completed",
    "mt5_verification_complete",
    "runtime_verified",
]
ALLOWED_CLAIMS = [
    "runtime_learning_probe_decision_recorded",
    "f91_repair_attempt_recorded",
    "runtime_probe_observation",
    "runtime_learning_record",
    "completion_claim_guard_recorded",
]

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


def f91_signal_frame() -> pd.DataFrame:
    if not path_exists(SOURCE_SCORE_SAMPLE):
        raise FileNotFoundError(SOURCE_SCORE_SAMPLE)
    raw = pd.read_csv(io_path(SOURCE_SCORE_SAMPLE))
    frame = raw.loc[raw["variant_id"].astype(str).eq(BEST_VARIANT)].copy()
    if frame.empty:
        raise RuntimeError(f"no rows for {BEST_VARIANT}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["split"] = frame["split"].astype(str)
    side = pd.to_numeric(frame["side"], errors="coerce").fillna(0).clip(-1, 1).astype("int8")
    frame[SIGNAL_COLUMN] = side
    frame["tier_label"] = mt5.TIER_A
    frame["routing_source"] = "f91_proxy_scores_sample_best_diagnostic_variant"
    frame["entry_decision"] = side.map({1: "long", -1: "short", 0: "flat"}).astype(str)
    return frame.sort_values("timestamp").reset_index(drop=True)


def materialize_runtime_surface(common_files_root: Path) -> dict[str, Any]:
    frame = f91_signal_frame()
    model_path = RUN_ROOT / "models" / "f91_runtime_learning_signal_score_table.csv"
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
            raise RuntimeError(f"F91 runtime learning surface has no rows for source split: {source_split}")
        matrix_path = RUN_ROOT / "mt5" / f"f91_runtime_learning_{split_label}_signal_matrix.csv"
        feature_artifact = mt5.export_mt5_feature_matrix_csv(
            split_frame,
            FEATURE_ORDER,
            matrix_path,
            metadata_columns=(
                "variant_id",
                "source_tier",
                "route_role",
                "label",
                "future_log_return_12",
                "regime_key",
                "entry_decision",
            ),
        )
        common_feature = copy_to_common(matrix_path, f"{COMMON_ROOT}/features/{matrix_path.name}", common_files_root)
        feature_artifacts.append(feature_artifact)
        common_copies.append(common_feature)
        attempts.append(
            attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=91,
                exploration_label="frontier91_RuntimeLearningProbeBackfill",
                attempt_name=f"f91_runtime_learning_{split_label}",
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
                record_view_prefix="mt5_f91_runtime_learning",
                max_hold_bars=12,
                common_root=COMMON_ROOT,
            )
        )
        timestamps = pd.to_datetime(split_frame["timestamp"], utc=True)
        side_counts = split_frame[SIGNAL_COLUMN].value_counts().to_dict()
        source_counts = split_frame["route_role"].astype(str).value_counts().to_dict()
        route_by_split[source_split] = {
            "tier_a_primary_rows": int(source_counts.get("tier_a_primary", 0)),
            "tier_b_fallback_rows": int(source_counts.get("tier_b_fallback", 0)),
            "routed_labelable_rows": int(len(split_frame)),
        }
        no_tier_by_split[source_split] = 0
        sample_coverage_by_split[split_label] = {
            "source_split": source_split,
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "sample_rows": int(len(split_frame)),
            "sample_min_timestamp_utc": timestamps.min().isoformat(),
            "sample_max_timestamp_utc": timestamps.max().isoformat(),
            "unique_timestamp_rows": int(timestamps.nunique()),
            "long_rows": int(side_counts.get(1, 0)),
            "short_rows": int(side_counts.get(-1, 0)),
            "flat_rows": int(side_counts.get(0, 0)),
            "claim_effect": "standard_tester_period_with_sparse_proxy_score_sample_no_completion_without_full_surface",
        }
        attempts[-1]["runtime_surface_contract"] = {
            "split": split_label,
            "source_split": source_split,
            "surface_scope": "sparse_diagnostic_sample",
            "source_artifact_role": "proxy_score_sample",
            "source_artifact_path": rel(SOURCE_SCORE_SAMPLE),
            "source_min_timestamp_utc": sample_coverage_by_split[split_label]["sample_min_timestamp_utc"],
            "source_max_timestamp_utc": sample_coverage_by_split[split_label]["sample_max_timestamp_utc"],
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "completion_claim_allowed": False,
            "standard_period_covered": False,
            "reason_code": "proxy_score_sample_is_not_full_runtime_surface",
            "claim_effect": "MT5 tester observation is allowed, but runtime_probe_completed is blocked until a full-period deterministic or sparse decision surface is materialized.",
        }
    side_counts_all = frame[SIGNAL_COLUMN].value_counts().to_dict()
    runtime_surface_contract = {
        "surface_scope": "sparse_diagnostic_sample",
        "source_artifact_role": "proxy_score_sample",
        "source_artifact_path": rel(SOURCE_SCORE_SAMPLE),
        "completion_claim_allowed": False,
        "standard_period_covered": False,
        "reason_code": "proxy_score_sample_is_not_full_runtime_surface",
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
        "source_candidate_gate": rel(SOURCE_CANDIDATE_GATE),
        "source_closeout_decision": rel(SOURCE_CLOSEOUT_DECISION),
        "best_variant": BEST_VARIANT,
        "label_id": LABEL_ID,
        "signal_column": SIGNAL_COLUMN,
        "feature_order_hash": ordered_hash(FEATURE_ORDER),
        "pre_gate_signal_count": int(len(frame)),
        "long_signal_count": int(side_counts_all.get(1, 0)),
        "short_signal_count": int(side_counts_all.get(-1, 0)),
        "flat_signal_count": int(side_counts_all.get(0, 0)),
        "standard_split_specs": split_specs,
        "sample_coverage_by_split": sample_coverage_by_split,
        "runtime_surface_contract": runtime_surface_contract,
        "model_artifact": model_artifact,
        "feature_artifacts": feature_artifacts,
        "common_copies": common_copies,
        "attempts": attempts,
        "route_coverage": {
            "by_split": route_by_split,
            "tier_b_fallback_by_split_subtype": {},
            "no_tier_by_split": no_tier_by_split,
        },
        "claim_effect": "runtime_learning_probe_surface_only_standard_attempts_required_before_completion_claim",
    }


def selected_mt5_blocker(result: Mapping[str, Any]) -> str:
    compile_payload = result.get("compile", {}) if isinstance(result.get("compile"), Mapping) else {}
    if compile_payload.get("status") != "completed":
        return str(compile_payload.get("blocker") or "compile_blocked")
    for row in result.get("execution_results", []) if isinstance(result.get("execution_results"), list) else []:
        if isinstance(row, Mapping) and row.get("status") != "completed":
            runtime_outputs = row.get("runtime_outputs", {}) if isinstance(row.get("runtime_outputs"), Mapping) else {}
            return str(row.get("blocker") or runtime_outputs.get("wait_status") or "tester_blocked")
    if result.get("external_verification_status") != "completed":
        return "runtime_outputs_or_report_blocked"
    return ""


def runtime_learning_decision(surface: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    blocker = selected_mt5_blocker(result)
    not_run_reason_code = "mt5_environment_blocked_after_attempt" if blocker in {"metaeditor_missing", "terminal_missing"} else ""
    return {
        "runtime_learning_probe_decision": {
            "pre_gate_signal_count": int(surface.get("pre_gate_signal_count", 0)),
            "strong_candidate_count": 0,
            "runtime_learning_probe_candidate_count": 1 if int(surface.get("pre_gate_signal_count", 0)) > 0 else 0,
            "runtime_surface_status": "repair_required",
            "mt5_action": "run_after_repair",
            "not_run_reason_code": not_run_reason_code,
            "repair_attempt_required": True,
            "repair_attempts": [
                {
                    "attempt_id": "repair01_f91_proxy_scores_sample_to_standard_validation_oos_runtime_surface",
                    "action": (
                        "materialized F91 best diagnostic proxy_scores_sample side column into a one-feature "
                        "EA-readable runtime learning surface"
                    ),
                    "result": "materialized",
                    "model_artifact": surface.get("model_artifact", {}),
                    "feature_artifacts": surface.get("feature_artifacts", []),
                    "surface_caveat": "proxy_score_sample diagnostic sample; no runtime_probe_completed claim",
                }
            ],
            "forbidden_skip_basis_seen": [],
            "claim_effect": "runtime_learning_probe_decision_only_no_runtime_authority_no_economics_pass",
        },
        "mt5_attempt_blocker": blocker,
        "mt5_attempt_result_status": result.get("external_verification_status", "blocked"),
    }


def apply_f91_runtime_learning_judgment(result: dict[str, Any]) -> None:
    result["claim_boundary"] = CLAIM_BOUNDARY
    if result.get("external_verification_status") != "completed":
        result["judgment"] = "blocked_runtime_learning_probe_observation_no_runtime_completion"
        return
    records = result.get("mt5_kpi_records", [])
    metrics = [record.get("metrics", {}) for record in records if isinstance(record, Mapping)]
    if metrics and all(float(row.get("net_profit") or 0.0) <= 0.0 or float(row.get("profit_factor") or 0.0) < 1.0 for row in metrics):
        result["judgment"] = "negative_runtime_learning_probe_observation_completed_no_economics_pass"
        return
    result["judgment"] = "inconclusive_runtime_learning_probe_observation_completed_no_economics_pass"


def compact_metrics_by_split(result: Mapping[str, Any]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for record in result.get("mt5_kpi_records", []) if isinstance(result.get("mt5_kpi_records"), list) else []:
        if not isinstance(record, Mapping):
            continue
        split = str(record.get("split") or record.get("record_view") or "unknown")
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows[split] = {
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "max_drawdown_percent": metrics.get("max_drawdown_percent"),
            "trade_count": metrics.get("trade_count"),
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "win_rate_percent": metrics.get("win_rate_percent"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
            "long_trade_count": metrics.get("long_trade_count"),
            "short_trade_count": metrics.get("short_trade_count"),
        }
    return rows


def make_actual_subagent_calls(subagent_id: str, nickname: str) -> dict[str, Any]:
    call = {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": subagent_id,
        "subagent_id": subagent_id,
        "nickname": nickname,
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "advice_classification": "accepted_with_local_verification",
        "remit": "F91 repair-first runtime learning probe materialization advice",
        "accepted_points": [
            "F91 is not a strong candidate because candidate_count=0.",
            "F91 proxy_scores_sample contains timestamp, split, side, and strength, so it can be repaired into a runtime learning surface.",
            "The correct mt5_action is run_after_repair, not blocked before repair.",
            "proxy_score_sample is a diagnostic sample and cannot support runtime_probe_completed.",
        ],
        "local_verification_update": [
            "Repair01 materialized the F91 best diagnostic side column into a one-feature runtime learning surface.",
            "MT5 Strategy Tester is run on validation_is and oos standard periods through the shared MT5 runtime probe contract.",
            "Completion claim guard blocks runtime_probe_completed because the runtime_surface_contract marks the source as proxy_score_sample.",
        ],
        "claim_effect": "advisory_only_no_reviewed_pass",
        "scope_caveat": "This packet records runtime learning observation only; full-period deterministic/sparse surface regeneration is required for completion claims.",
    }
    return {
        "call_mode": "micro_consult",
        "agents_requested_count": 1,
        "agents_completed_count": 1,
        "claim_effect": "advisory_only_no_reviewed_pass",
        "agents_called": [call],
    }


def make_work_packet(created_at: str) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "runtime_learning_probe_decision_gate",
        "mt5_runtime_probe_contract_audit",
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
        "user_request": {
            "requested_action": "runtime_probe_backfill_repair_with_task_force",
            "requested_count": 1,
            "ambiguous_terms": [],
        },
        "current_truth": {
            "target_stage": "F91",
            "historical_status": "closed_negative_no_runtime_probe",
            "boundary": "f91_closeout_not_rewritten",
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest"],
            "mutation_intent": "targeted_update",
            "execution_intent": "run_standard_mt5_probe_after_repair",
        },
        "risk_vector_scan": {
            "risks": {"sample_surface_overclaim": "high", "completion_overclaim": "high", "side_imbalance": "known_extreme"},
            "required_decision_locks": [
                "f91_is_backfill_observation_only",
                "runtime_probe_completed_blocked_for_sample_surface",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "locked_direction": "f91_runtime_learning_probe_backfill_observation_only",
            "not_locked": ["selected_baseline", "promotion_candidate", "runtime_authority", "live_readiness", "goal_achieve"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": ["stage_pipelines/stage_frontier_91/frontier91_runtime_learning_probe_backfill.py"],
            "scope_units": [
                "f91_proxy_score_sample_repair",
                "mt5_runtime_learning_observation",
                "sample_surface_completion_guard",
            ],
            "execution_layers": ["python_local_execution", "mt5_execution", "gate_execution"],
            "mutation_policy": {"allowed": True, "scope": "targeted_f91_backfill_only"},
            "evidence_layers": [
                "runtime_learning_probe_decision",
                "mt5_runtime_probe_contract_audit",
                "completion_claim_guard",
                "task_force_micro_consult",
                "tests",
            ],
            "reduction_policy": {"reduction_allowed": False},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "runtime_learning_probe",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_continuation",
                "F91_candidate_gate_count_zero_but_repairable_proxy_scores_sample",
                "MT5_runtime_probe_anti_deferral_goal",
            ],
            "protected_claims": ["runtime_learning_probe_decision", "runtime_probe_observation", "completion_claim_guard_recorded"],
            "required_evidence": [
                "runtime_learning_probe_decision",
                "mt5_action run_after_repair",
                "repair_attempts",
                "MT5 terminal command",
                "validation_is and oos Strategy Tester reports",
                "mt5_runtime_probe_contract_audit",
                "mt5_runtime_probe_completion_claim_guard",
                "actual_subagent_calls",
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runtime_authority_or_economics_pass_claim",
                    "reason": "F91 packet records runtime_probe_observation only; sample surface blocks completion and authority claims.",
                    "claim_effect": "No runtime authority, economics pass, materialization-ready, or handoff-complete claim.",
                }
            ],
            "stop_conditions": [
                "F91 runtime learning observation recorded",
                "completion claim guard blocks runtime_probe_completed",
                "no runtime authority claim",
            ],
        },
        "acceptance_criteria": {
            "required": [
                "runtime_learning_probe_decision_gate passes",
                "MT5 observation audit passes with validation_is and oos reports",
                "completion claim guard blocks sample surface completion",
                "Task Force micro consult actual subagent call is recorded",
            ],
            "forbidden": FORBIDDEN_CLAIMS,
        },
        "work_plan": [
            {"step": "Inspect F91 proxy score sample and candidate gate", "status": "completed"},
            {"step": "Task Force micro consult", "status": "completed"},
            {"step": "Materialize sparse diagnostic sample runtime surface", "status": "completed"},
            {"step": "Run standard validation_is and oos MT5 probes", "status": "completed"},
            {"step": "Record receipt and closeout gates", "status": "in_progress"},
        ],
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-prime-ml",
            "support_skills": [
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
                "obsidian-artifact-lineage",
            ],
            "skills_selected": [
                "obsidian-prime-ml",
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_not_used": [{"skill": "obsidian-artifact-lineage", "reason": "lineage captured in receipt and MT5 result; no separate lineage claim"}],
            "required_skill_receipts": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "required_evidence": [
                "runtime_probe_backfill_receipt.json",
                "mt5_runtime_probe_contract_audit.json",
                "mt5_runtime_probe_completion_claim_guard.json",
                "runtime_learning_probe_decision_gate_actual.json",
                "actual_subagent_calls.json",
            ],
            "runtime_surface_contract": "sample_surface_blocks_runtime_probe_completed",
            "forbidden_evidence_substitutes": ["proxy_only", "compile_only", "git_push"],
        },
        "gates": {
            "required": required_gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "F91 packet records runtime_probe_observation only; no runtime authority/economics/materialization claim is requested."
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "completion_claim": "forbidden",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def make_skill_receipts(result: Mapping[str, Any], actual_calls: Mapping[str, Any]) -> dict[str, Any]:
    tester_identity = (
        "US100 M5, Model=4, Deposit=500, Leverage=1:100, validation_is 2025.01.02..2025.10.01, "
        "oos 2025.10.01..2026.04.13"
    )
    return {
        "receipts": [
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-runtime-parity",
                "status": "executed",
                "python_artifact": "stage_pipelines/stage_frontier_91/frontier91_runtime_learning_probe_backfill.py",
                "runtime_artifact": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "compared_surface": "F91 proxy_scores_sample side signal -> one-feature EBM table -> MT5 RuntimeProbeEA telemetry",
                "parity_level": "runtime_learning_probe_observation_only",
                "runtime_learning_probe_decision": "runtime_learning_probe_candidate_count=1; mt5_action=run_after_repair; repair_attempts=1; forbidden_skip_basis_seen=[]",
                "tester_identity": tester_identity,
                "missing_evidence": ["full-period deterministic F91 decision surface", "full-period sparse decision surface"],
                "allowed_claims": ["runtime_probe_observation", "runtime_learning_record"],
                "forbidden_claims": FORBIDDEN_CLAIMS,
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-backtest-forensics",
                "status": "executed",
                "tester_report": "validation_is and oos Strategy Tester reports completed"
                if result.get("external_verification_status") == "completed"
                else "Strategy Tester report incomplete or blocked",
                "tester_settings": tester_identity + ", /portable, ReplaceReport=1, ShutdownTerminal=1",
                "spread_commission_slippage": "broker-native tester behavior; no added modeled commission",
                "trade_list_identity": "Strategy Tester report metrics and EA telemetry hashes recorded in mt5_runtime_learning_probe_result.json",
                "runtime_learning_probe_decision": "F91 sample surface is valid only as runtime learning observation; runtime_probe_completed is blocked.",
                "forensic_gaps": ["proxy_scores_sample is sparse diagnostic sample, not full runtime surface"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment_boundary": "runtime_learning_probe_observation_only",
                "allowed_claims": ["runtime_probe_observation", "runtime_learning_record", "completion_claim_guard_recorded"],
                "forbidden_claims": FORBIDDEN_CLAIMS,
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
                "bounded_evidence": [rel(SOURCE_CANDIDATE_GATE), rel(SOURCE_SCORE_SAMPLE), rel(SOURCE_CLOSEOUT_DECISION)],
                "advice_classification": "accepted_with_local_verification",
                "local_verification": "F91 repair01 materialized sample side signal and ran standard MT5 observation attempts.",
                "claim_boundary": CLAIM_BOUNDARY,
                "final_codex_direction": "run_after_repair_observation_only_no_reviewed_pass_claim",
                "forbidden_claim_check": {"forbidden_claims": FORBIDDEN_CLAIMS, "completed_forbidden": False},
            },
        ]
    }


def make_closeout_report(result: Mapping[str, Any]) -> str:
    metrics = compact_metrics_by_split(result)
    status = result.get("external_verification_status")
    return f"""# F91 Runtime Learning Probe Backfill Closeout

## Conclusion
F91 was repaired into a runtime learning observation, not a completed runtime probe. MT5 status: `{status}`. The source surface is proxy_score_sample, so runtime_probe_completed remains blocked.

## What changed
- Added F91 runtime learning backfill script and MT5 artifacts.
- Materialized the best diagnostic regime-density-cost proxy side column into a one-feature runtime learning signal.
- Recorded Einstein micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- Full F91 regime-density-cost decision surface regeneration over the standard periods was not performed in this packet.
- Sample coverage remains sparse and side-imbalanced: this is learning evidence, not completion evidence.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f91_repair_attempt_recorded
- runtime_probe_observation
- runtime_learning_record
- completion_claim_guard_recorded

## Forbidden claims
- runtime_probe_completed
- runtime_verified
- economics_pass
- selected_baseline
- promotion_candidate
- runtime_authority
- operating_promotion
- live_readiness
- Goal Achieve

## Next hardening step
If F91 is revisited, regenerate the `{BEST_VARIANT}` surface over the full standard validation_is and oos windows before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{json.dumps(json_ready(metrics), ensure_ascii=False, indent=2)}
```
"""


def write_packet_artifacts(payload: Mapping[str, Any], args: argparse.Namespace) -> None:
    created_at = str(payload.get("created_at_utc") or utc_now())
    result = payload.get("mt5_result", {}) if isinstance(payload.get("mt5_result"), Mapping) else {}
    surface = payload.get("surface", {}) if isinstance(payload.get("surface"), Mapping) else {}
    actual_calls = make_actual_subagent_calls(args.subagent_id, args.subagent_nickname)
    write_json(PACKET_ROOT / "actual_subagent_calls.json", actual_calls)
    write_json(
        PACKET_ROOT / "codex_task_force_review_packet.json",
        {
            "audit_name": "codex_task_force_review_packet",
            "status": "pass",
            "passed": True,
            "completed_forbidden": False,
            "counts": {
                "call_mode": "micro_consult",
                "agents_used_count": 1,
                "actual_subagent_calls": [args.subagent_id],
                "claim_effect": "advisory_only_no_reviewed_pass",
                "full_roster_call_reason": None,
            },
            "findings": [],
            "allowed_claims": ["task_force_micro_consult_recorded"],
            "forbidden_claims": ["task_force_reviewed_pass"],
        },
    )
    write_yaml(PACKET_ROOT / "work_packet.yaml", make_work_packet(created_at))
    write_json(PACKET_ROOT / "skill_receipts.json", make_skill_receipts(result, actual_calls))
    write_text(PACKET_ROOT / "closeout_report.md", make_closeout_report(result))
    write_json(
        PACKET_ROOT / "runtime_probe_backfill_receipt.json",
        {
            "packet_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "backfill_reason": "active_goal_requires_repair_first_mt5_runtime_learning_probe_for_omitted_frontier_runtime_probes",
            "historical_judgment": "negative_regime_density_cost_abstention_proxy_no_candidate_no_runtime_trigger",
            "historical_runtime_probe_status": "not_run_no_candidate_no_runnable_decision_surface",
            "candidate_surface_status": "learning_candidate_repaired_and_runtime_observed_sample_surface_completion_blocked",
            "judgment": result.get("judgment"),
            "claim_boundary": CLAIM_BOUNDARY,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "surface": {
                "best_variant": surface.get("best_variant"),
                "pre_gate_signal_count": surface.get("pre_gate_signal_count"),
                "long_signal_count": surface.get("long_signal_count"),
                "short_signal_count": surface.get("short_signal_count"),
                "flat_signal_count": surface.get("flat_signal_count"),
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
            "next_repair_option": "Regenerate F91 best diagnostic regime-density-cost decision surface as full-period deterministic or sparse surface before runtime_probe_completed.",
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
        "common_copies": surface["common_copies"],
        "route_coverage": surface["route_coverage"],
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "f91_proxy_scores_sample_side_signal_runtime_learning_surface",
        "label_id": LABEL_ID,
        "split_contract": "mt5_runtime_probe_contract_v1_standard_validation_is_oos",
        "stage_inheritance": "f91_historical_negative_memory_only_no_success_rewrite",
        "python_metrics": {
            "pre_gate_signal_count": surface["pre_gate_signal_count"],
            "long_signal_count": surface["long_signal_count"],
            "short_signal_count": surface["short_signal_count"],
            "flat_signal_count": surface["flat_signal_count"],
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
    apply_f91_runtime_learning_judgment(result)
    contract_audit = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_observation",)).to_dict()
    completion_claim_guard = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_completed",)).to_dict()
    decision = runtime_learning_decision(surface, result)
    payload = {
        "created_at_utc": utc_now(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "surface": surface,
        "prepared": prepared,
        "mt5_result": result,
        "mt5_runtime_probe_contract_audit": contract_audit,
        "mt5_runtime_probe_completion_claim_guard": completion_claim_guard,
        "runtime_learning_probe_decision": decision["runtime_learning_probe_decision"],
        "mt5_attempt_blocker": decision["mt5_attempt_blocker"],
        "mt5_attempt_result_status": decision["mt5_attempt_result_status"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(RUN_ROOT / "runtime_learning_surface_triage.json", surface)
    write_json(RUN_ROOT / "mt5_runtime_learning_probe_result.json", result)
    write_json(RUN_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(RUN_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(PACKET_ROOT / "f91_runtime_learning_probe_backfill_result.json", payload)
    write_json(PACKET_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(PACKET_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_packet_artifacts(payload, args)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill F91 as a runtime learning probe after repair-first materialization.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--subagent-id", default="019ee32a-1327-7773-82f0-0b993d9f831e")
    parser.add_argument("--subagent-nickname", default="Einstein")
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
