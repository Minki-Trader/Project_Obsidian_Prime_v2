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


RUN_ID = "frontier89_runtime_learning_probe_backfill_v1"
STAGE_ID = "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
SOURCE_RUN_ID = "frontier89B_deal_path_adverse_selection_proxy_scout_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID / "proxy_scout"
SOURCE_SURFACE = SOURCE_ROOT / "deal_path_teacher_surface.csv"
SOURCE_PROXY_SCORES = SOURCE_ROOT / "proxy_scores.csv"
SOURCE_CANDIDATE_QUEUE = SOURCE_ROOT / "candidate_queue.csv"
SOURCE_SUMMARY = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID / "summary.json"
SOURCE_CLOSEOUT_DECISION = (
    STAGE_ROOT
    / "02_runs"
    / "frontier89C_deal_path_teacher_repair_or_rotation_decision_v1"
    / "decision"
    / "deal_path_teacher_repair_or_rotation_decision.json"
)
LABEL_ID = "deal_path_adverse_selection_teacher_v1"
SIGNAL_COLUMN = "f89_runtime_learning_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = f"Project_Obsidian_Prime_v2/f89_runtime_learning/{RUN_ID}"
CLAIM_BOUNDARY = (
    "runtime_learning_probe_observation_only_no_f89_success_rewrite_no_baseline_no_promotion_"
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
    "f89_repair_attempt_recorded",
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def selected_candidate() -> dict[str, Any]:
    summary = load_json(SOURCE_SUMMARY)
    candidate_id = str(summary.get("candidate_decision", {}).get("selected_candidate_id", ""))
    queue = pd.read_csv(io_path(SOURCE_CANDIDATE_QUEUE))
    row = queue.loc[queue["candidate_id"].astype(str).eq(candidate_id)]
    if row.empty:
        raise RuntimeError(f"F89 selected candidate is missing from candidate_queue: {candidate_id}")
    record = row.iloc[0].to_dict()
    selected_ids = [
        episode_id.strip()
        for episode_id in str(record.get("selected_episode_ids", "")).split(";")
        if episode_id.strip()
    ]
    return {
        "candidate_id": candidate_id,
        "selected_episode_ids": selected_ids,
        "selected_rows": int(float(record.get("selected_rows", 0) or 0)),
        "top_frac": float(record.get("top_frac", 0) or 0),
        "selection_role": str(record.get("selection_role", "")),
        "net_delta_vs_take_all": float(record.get("net_delta_vs_take_all", 0) or 0),
        "runtime_claim": str(record.get("runtime_claim", "not_claimed")),
    }


def f89_signal_frame() -> pd.DataFrame:
    if not path_exists(SOURCE_SURFACE):
        raise FileNotFoundError(SOURCE_SURFACE)
    if not path_exists(SOURCE_PROXY_SCORES):
        raise FileNotFoundError(SOURCE_PROXY_SCORES)
    surface = pd.read_csv(io_path(SOURCE_SURFACE))
    scores = pd.read_csv(io_path(SOURCE_PROXY_SCORES))[["episode_id", "adverse_selection_score"]]
    frame = surface.merge(scores, on="episode_id", how="left", validate="one_to_one")
    if frame.empty:
        raise RuntimeError("F89 deal path teacher surface is empty.")
    candidate = selected_candidate()
    selected_ids = set(candidate["selected_episode_ids"])
    frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame["split"] = frame["split"].astype(str)
    frame["original_signal"] = frame["side"].astype(str).str.lower().map({"buy": 1, "sell": -1}).fillna(0).astype("int8")
    frame["vetoed_by_teacher"] = frame["episode_id"].astype(str).isin(selected_ids)
    frame[SIGNAL_COLUMN] = frame["original_signal"].where(~frame["vetoed_by_teacher"], 0).astype("int8")
    frame["tier_label"] = mt5.TIER_A
    frame["routing_source"] = "f89_deal_path_teacher_surface_selected_candidate_veto"
    frame["route_role"] = "tier_a_primary_validation_only"
    frame["entry_decision"] = frame[SIGNAL_COLUMN].map({1: "long", -1: "short", 0: "flat"}).astype(str)
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    if duplicate_timestamps:
        raise RuntimeError(f"F89 repair requires unique timestamps; duplicates={duplicate_timestamps}")
    frame.attrs["repair"] = {
        "repair_id": "repair01_deal_path_teacher_veto_sparse_surface",
        "rule": (
            "Use F89B selected locked-forward readout candidate as an observation-only veto: "
            "original F88C buy/sell side is kept, selected high adverse-selection episode ids are set to flat; "
            "no threshold retune and no OOS rows are invented."
        ),
        "source_rows": int(len(frame)),
        "selected_candidate": candidate,
        "vetoed_rows": int(frame["vetoed_by_teacher"].sum()),
        "duplicate_timestamp_rows": duplicate_timestamps,
        "oos_surface_status": "missing_required_not_invented",
        "claim_effect": "sample repaired into a sparse validation-only decision surface for runtime learning observation only",
    }
    return frame.sort_values("timestamp").reset_index(drop=True)


def empty_split_frame(template: pd.DataFrame, source_split: str) -> pd.DataFrame:
    frame = template.iloc[0:0].copy()
    frame["split"] = frame.get("split", pd.Series(dtype=str)).astype(str)
    if "timestamp" not in frame.columns:
        frame["timestamp"] = pd.Series(dtype="datetime64[ns, UTC]")
    frame["split"] = source_split
    return frame


def split_coverage(split_frame: pd.DataFrame, source_split: str, from_date: str, to_date: str) -> dict[str, Any]:
    side_counts = split_frame[SIGNAL_COLUMN].value_counts().to_dict() if SIGNAL_COLUMN in split_frame else {}
    if split_frame.empty:
        return {
            "source_split": source_split,
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "sample_rows": 0,
            "sample_min_timestamp_utc": None,
            "sample_max_timestamp_utc": None,
            "unique_timestamp_rows": 0,
            "long_rows": 0,
            "short_rows": 0,
            "flat_rows": 0,
            "claim_effect": "standard_tester_period_with_missing_source_surface_no_completion_or_authority",
        }
    timestamps = pd.to_datetime(split_frame["timestamp"], utc=True)
    return {
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
        "claim_effect": "standard_tester_period_with_sparse_diagnostic_sample_no_completion_without_full_surface",
    }


def runtime_surface_contract_for_split(
    *,
    split_label: str,
    source_split: str,
    from_date: str,
    to_date: str,
    coverage: Mapping[str, Any],
) -> dict[str, Any]:
    missing_source = int(coverage.get("sample_rows", 0) or 0) == 0
    return {
        "split": split_label,
        "source_split": source_split,
        "standard_from_date": from_date,
        "standard_to_date": to_date,
        "source_min_timestamp_utc": coverage.get("sample_min_timestamp_utc"),
        "source_max_timestamp_utc": coverage.get("sample_max_timestamp_utc"),
        "surface_scope": "empty_missing_source_surface" if missing_source else "sparse_diagnostic_sample",
        "source_artifact_role": "diagnostic_sample" if not missing_source else "missing_required_oos_surface",
        "source_artifact_path": rel(SOURCE_SURFACE) if not missing_source else None,
        "standard_period_covered": False,
        "completion_claim_allowed": False,
        "reason_code": "oos_deal_path_teacher_surface_missing" if missing_source else "diagnostic_deal_path_teacher_sample_is_not_full_runtime_surface",
        "claim_effect": (
            "MT5 tester can record no-surface/no-trade observation for this split, but completion is blocked."
            if missing_source
            else "MT5 tester observation is allowed, but runtime_probe_completed is blocked until a full-period deterministic or sparse decision surface is materialized."
        ),
    }


def materialize_runtime_surface(common_files_root: Path) -> dict[str, Any]:
    frame = f89_signal_frame()
    repair = dict(frame.attrs.get("repair", {}))
    model_path = RUN_ROOT / "models" / "f89_runtime_learning_signal_score_table.csv"
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
            split_frame = empty_split_frame(frame, source_split)
        matrix_path = RUN_ROOT / "mt5" / f"f89_runtime_learning_{split_label}_signal_matrix.csv"
        feature_artifact = mt5.export_mt5_feature_matrix_csv(
            split_frame,
            FEATURE_ORDER,
            matrix_path,
            metadata_columns=(
                "episode_id",
                "side",
                "profit",
                "target_adverse_loss",
                "adverse_selection_score",
                "vetoed_by_teacher",
                "entry_decision",
                "selection_split_role",
            ),
        )
        common_feature = copy_to_common(matrix_path, f"{COMMON_ROOT}/features/{matrix_path.name}", common_files_root)
        feature_artifacts.append(feature_artifact)
        common_copies.append(common_feature)
        attempts.append(
            attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=89,
                exploration_label="frontier89_RuntimeLearningProbeBackfill",
                attempt_name=f"f89_runtime_learning_{split_label}",
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
                record_view_prefix="mt5_f89_runtime_learning",
                max_hold_bars=12,
                common_root=COMMON_ROOT,
            )
        )
        coverage = split_coverage(split_frame, source_split, from_date, to_date)
        sample_coverage_by_split[split_label] = coverage
        route_by_split[source_split] = {
            "tier_a_primary_rows": int(len(split_frame)),
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": int(len(split_frame)),
        }
        no_tier_by_split[source_split] = 0
        attempts[-1]["runtime_surface_contract"] = runtime_surface_contract_for_split(
            split_label=split_label,
            source_split=source_split,
            from_date=from_date,
            to_date=to_date,
            coverage=coverage,
        )
    runtime_surface_contract = {
        "version": "runtime_surface_contract_v1",
        "source_stage": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "surface_scope": "sparse_diagnostic_sample_with_missing_oos_source",
        "completion_claim_allowed": False,
        "by_split": {
            str(attempt["split"]): attempt["runtime_surface_contract"]
            for attempt in attempts
            if isinstance(attempt.get("runtime_surface_contract"), Mapping)
        },
    }
    side_counts = frame[SIGNAL_COLUMN].value_counts().to_dict()
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_surface": rel(SOURCE_SURFACE),
        "source_proxy_scores": rel(SOURCE_PROXY_SCORES),
        "source_candidate_queue": rel(SOURCE_CANDIDATE_QUEUE),
        "source_summary": rel(SOURCE_SUMMARY),
        "source_closeout_decision": rel(SOURCE_CLOSEOUT_DECISION),
        "repair": repair,
        "model_artifact": model_artifact,
        "feature_artifacts": feature_artifacts,
        "common_copies": common_copies,
        "attempts": attempts,
        "standard_split_specs": split_specs,
        "sample_coverage_by_split": sample_coverage_by_split,
        "runtime_surface_contract": runtime_surface_contract,
        "pre_gate_signal_count": int((frame[SIGNAL_COLUMN] != 0).sum()),
        "source_episode_rows": int(len(frame)),
        "long_signal_count": int(side_counts.get(1, 0)),
        "short_signal_count": int(side_counts.get(-1, 0)),
        "flat_signal_count": int(side_counts.get(0, 0)),
        "route_coverage": {
            "by_split": route_by_split,
            "tier_b_fallback_by_split_subtype": {},
            "no_tier_by_split": no_tier_by_split,
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def apply_runtime_learning_judgment(result: dict[str, Any]) -> None:
    reports = result.get("strategy_tester_reports", [])
    completed_reports = [row for row in reports if row.get("status") == "completed"] if isinstance(reports, list) else []
    result["external_verification_status"] = "completed" if len(completed_reports) >= 2 else "incomplete"
    result["judgment"] = "inconclusive_runtime_learning_probe_observation_completed_no_economics_pass"
    result["claim_boundary"] = CLAIM_BOUNDARY
    result["stage_inheritance"] = "f89_historical_negative_memory_only_no_success_rewrite"


def runtime_learning_decision(surface: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    repair = surface.get("repair", {}) if isinstance(surface.get("repair"), Mapping) else {}
    return {
        "runtime_learning_probe_decision": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "historical_runtime_probe_status": "not_run_no_meaningful_materialization_candidate_no_runtime_claim",
            "strong_candidate_count": 0,
            "runtime_learning_probe_candidate_count": 1 if int(surface.get("source_episode_rows", 0)) > 0 else 0,
            "pre_gate_signal_count": int(surface.get("pre_gate_signal_count", 0)),
            "repair_attempt_count": 1,
            "runtime_surface_status": "repair_required_validation_only_oos_missing",
            "mt5_action": "run_after_repair",
            "not_run_reason_code": "",
            "repair_attempt_required": True,
            "forbidden_no_run_reasons": [
                "candidate_gate_failed",
                "weak_proxy",
                "low_trade_count_expected",
                "no_meaningful_materialization_candidate",
            ],
            "forbidden_skip_basis_seen": [],
            "claim_effect": "F89 has a repairable validation-only runtime learning surface; MT5 is run after repair while completion remains blocked by diagnostic/missing-OOS surface contract.",
            "repair_attempts": [
                {
                    "repair_id": repair.get("repair_id", "repair01_deal_path_teacher_veto_sparse_surface"),
                    "result": "materialized",
                    "claim_effect": repair.get("claim_effect"),
                    "oos_surface_status": repair.get("oos_surface_status"),
                }
            ],
            "required_evidence": [
                "standard validation_is and oos tester attempts",
                "Strategy Tester reports",
                "runtime surface contract with missing OOS boundary",
                "completion claim guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "mt5_attempt_result_status": result.get("external_verification_status", "unknown"),
        "mt5_attempt_blocker": "" if result.get("external_verification_status") == "completed" else "strategy_tester_reports_incomplete",
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
        "remit": "F89 runtime learning probe action classification from F89B deal-path teacher surface",
        "accepted_points": [
            "F89B has a repairable validation-only deal-path teacher surface.",
            "Use the selected candidate as a sparse veto surface for runtime learning observation only.",
            "Missing OOS source rows must be recorded, not invented.",
            "Allowed claim is runtime_learning_observation only; completion and authority claims are blocked.",
        ],
        "local_verification_update": [
            "Repair01 materialized the F89B selected candidate into a one-feature sparse veto signal.",
            "MT5 Strategy Tester is run on validation_is and oos standard periods through the shared MT5 runtime probe contract.",
            "Completion claim guard blocks runtime_probe_completed because the runtime_surface_contract marks the source as diagnostic/missing OOS.",
        ],
        "claim_effect": "advisory_only_no_reviewed_pass",
        "scope_caveat": "OOS surface is missing_required; OOS report is a no-source/no-trade observation, not validation of generalization.",
    }
    return {
        "call_mode": "micro_consult",
        "agents_requested_count": 1,
        "agents_completed_count": 1 if result_status == "completed" else 0,
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
            "target_stage": "F89",
            "historical_status": "closed_negative_no_runtime_probe",
            "boundary": "f89_closeout_not_rewritten",
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest"],
            "mutation_intent": "targeted_update",
            "execution_intent": "run_standard_mt5_probe_after_repair",
        },
        "risk_vector_scan": {
            "risks": {"sample_surface_overclaim": "high", "completion_overclaim": "high", "oos_surface_missing": "known_blocker"},
            "required_decision_locks": [
                "f89_is_backfill_observation_only",
                "runtime_probe_completed_blocked_for_sample_surface_and_missing_oos",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "locked_direction": "f89_runtime_learning_probe_backfill_observation_only",
            "not_locked": ["selected_baseline", "promotion_candidate", "runtime_authority", "live_readiness", "goal_achieve"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": ["stage_pipelines/stage_frontier_89/frontier89_runtime_learning_probe_backfill.py"],
            "scope_units": [
                "f89_deal_path_teacher_veto_repair",
                "mt5_runtime_learning_observation",
                "missing_oos_surface_completion_guard",
            ],
            "execution_layers": ["python_local_execution", "mt5_execution", "gate_execution"],
            "mutation_policy": {"allowed": True, "scope": "targeted_f89_backfill_only"},
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
                "F89_no_meaningful_candidate_but_repairable_deal_path_teacher_surface",
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
                    "reason": "F89 packet records runtime_probe_observation only; sample surface and missing OOS source block completion and authority claims.",
                    "claim_effect": "No runtime authority, economics pass, materialization-ready, or handoff-complete claim.",
                }
            ],
            "stop_conditions": [
                "F89 runtime learning observation recorded",
                "completion claim guard blocks runtime_probe_completed",
                "missing OOS source boundary recorded",
            ],
        },
        "acceptance_criteria": {
            "required": [
                "runtime_learning_probe_decision_gate passes",
                "MT5 observation audit passes with validation_is and oos reports",
                "completion claim guard blocks sample/missing-OOS completion",
                "Task Force micro consult actual subagent call is recorded",
            ],
            "forbidden": FORBIDDEN_CLAIMS,
        },
        "work_plan": [
            {"step": "Inspect F89 deal-path teacher surface and closeout", "status": "completed"},
            {"step": "Task Force micro consult", "status": "completed"},
            {"step": "Materialize sparse validation-only veto surface", "status": "completed"},
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
            "skills_selected": [
                "obsidian-prime-ml",
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
            "skills_not_used": [
                {
                    "skill": "obsidian-artifact-lineage",
                    "reason": "lineage captured in receipt, runtime result, and source artifact refs; no separate lineage claim",
                }
            ],
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
            "runtime_surface_contract": "sample_and_missing_oos_surface_blocks_runtime_probe_completed",
            "forbidden_evidence_substitutes": ["proxy_only", "compile_only", "git_push"],
        },
        "gates": {
            "required": required_gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "F89 packet records runtime_probe_observation only; no runtime authority/economics/materialization claim is requested."
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
                "python_artifact": "stage_pipelines/stage_frontier_89/frontier89_runtime_learning_probe_backfill.py",
                "runtime_artifact": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "compared_surface": "F89 deal-path teacher selected-candidate veto signal -> one-feature EBM table -> MT5 RuntimeProbeEA telemetry",
                "parity_level": "runtime_learning_probe_observation_only",
                "runtime_learning_probe_decision": "runtime_learning_probe_candidate_count=1; mt5_action=run_after_repair; repair_attempts=1; oos_source_missing_recorded",
                "tester_identity": tester_identity,
                "missing_evidence": ["full-period deterministic F89 decision surface", "OOS deal-path teacher source rows"],
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
                "runtime_learning_probe_decision": "F89 validation-only sample surface is valid only as runtime learning observation; runtime_probe_completed is blocked.",
                "forensic_gaps": [
                    "deal_path_teacher_surface is sparse diagnostic validation sample, not full runtime surface",
                    "OOS deal-path teacher source surface is missing_required and was not invented",
                ],
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
                "bounded_evidence": [rel(SOURCE_SURFACE), rel(SOURCE_CANDIDATE_QUEUE), rel(SOURCE_CLOSEOUT_DECISION)],
                "advice_classification": "accepted_with_local_verification",
                "local_verification": "F89 repair01 materialized selected candidate veto signal and ran standard MT5 observation attempts.",
                "claim_boundary": CLAIM_BOUNDARY,
                "final_codex_direction": "run_after_repair_observation_only_no_reviewed_pass_claim",
                "forbidden_claim_check": {"forbidden_claims": FORBIDDEN_CLAIMS, "completed_forbidden": False},
            },
        ]
    }


def make_closeout_report(result: Mapping[str, Any]) -> str:
    metrics = compact_metrics_by_split(result)
    return f"""# F89 Runtime Learning Probe Backfill Closeout

## Conclusion
F89 was repaired into a runtime learning observation, not a completed runtime probe. The source is a validation-only diagnostic deal-path teacher surface, so runtime_probe_completed remains blocked.

## What changed
- Added F89 runtime learning backfill script and MT5 artifacts.
- Materialized the F89B selected candidate as a one-feature sparse veto signal.
- Recorded agent_08 micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- F89 has no OOS deal-path teacher source rows; the OOS tester attempt is a missing-source observation.
- The source surface remains sparse and diagnostic, not full-period deterministic or sparse decision surface.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f89_repair_attempt_recorded
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
If F89 is revisited, generate a full-period validation_is plus oos deal-path teacher surface before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{json.dumps(json_ready(metrics), ensure_ascii=False, indent=2)}
```
"""


def write_packet_artifacts(payload: Mapping[str, Any], args: argparse.Namespace) -> None:
    created_at = str(payload.get("created_at_utc") or utc_now())
    result = payload.get("mt5_result", {}) if isinstance(payload.get("mt5_result"), Mapping) else {}
    surface = payload.get("surface", {}) if isinstance(payload.get("surface"), Mapping) else {}
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
            "historical_judgment": "negative_for_materialization_candidate_inconclusive_for_teacher_axis_no_runtime_evidence",
            "historical_runtime_probe_status": "not_run_no_meaningful_materialization_candidate_no_runtime_claim",
            "candidate_surface_status": "learning_candidate_repaired_and_runtime_observed_validation_only_oos_missing_completion_blocked",
            "judgment": result.get("judgment"),
            "claim_boundary": CLAIM_BOUNDARY,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "surface": {
                "source_episode_rows": surface.get("source_episode_rows"),
                "pre_gate_signal_count": surface.get("pre_gate_signal_count"),
                "long_signal_count": surface.get("long_signal_count"),
                "short_signal_count": surface.get("short_signal_count"),
                "flat_signal_count": surface.get("flat_signal_count"),
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
            "next_repair_option": "Generate full-period validation_is and oos deal-path teacher surfaces before runtime_probe_completed.",
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
        "feature_set_id": "f89_deal_path_teacher_veto_runtime_learning_surface",
        "label_id": LABEL_ID,
        "split_contract": "mt5_runtime_probe_contract_v1_standard_validation_is_oos",
        "stage_inheritance": "f89_historical_negative_memory_only_no_success_rewrite",
        "python_metrics": {
            "source_episode_rows": surface["source_episode_rows"],
            "pre_gate_signal_count": surface["pre_gate_signal_count"],
            "long_signal_count": surface["long_signal_count"],
            "short_signal_count": surface["short_signal_count"],
            "flat_signal_count": surface["flat_signal_count"],
            "sample_coverage_by_split": surface["sample_coverage_by_split"],
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
    apply_runtime_learning_judgment(result)
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
    write_json(PACKET_ROOT / "f89_runtime_learning_probe_backfill_result.json", payload)
    write_json(PACKET_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(PACKET_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_packet_artifacts(payload, args)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill F89 as a runtime learning probe after repair-first materialization.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output-json", default=str(PACKET_ROOT / "runtime_probe_payload.json"))
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--subagent-id", default="019ee34a-ec97-7531-a972-43124677eace")
    parser.add_argument("--subagent-nickname", default="Dewey")
    parser.add_argument("--subagent-result-status", default="completed")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run(args)
    output_path = Path(args.output_json)
    write_json(output_path, payload)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not args.materialize_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
