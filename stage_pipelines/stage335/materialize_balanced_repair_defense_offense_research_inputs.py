from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335P"
RUN_ID = "run335P_materialize_balanced_repair_defense_offense_research_inputs_v1"
PARENT_RUN_ID = "run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1"
NEXT_RUN_ID = "run335Q_review_balanced_repair_defense_offense_research_inputs_v1"

STATUS = "completed_balanced_repair_defense_offense_inputs_materialized_no_forward_decision"
JUDGMENT = "repair_defense_offense_inputs_materialized_usable_for_next_review_no_selection"
DECISION = "stage335P_balanced_inputs_materialized_proxy_blocked_exact_join_repair_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335P_balanced_repair_defense_offense_inputs_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN335K_DIR = STAGE_DIR / "02_runs" / "run335K"
RUN335N_DIR = STAGE_DIR / "02_runs" / "run335N"
RUN335O_DIR = STAGE_DIR / "02_runs" / "run335O"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335P_balanced_repair_defense_offense_inputs.md"
REPORT_DOC = REVIEWS_DIR / "run335P_balanced_repair_defense_offense_inputs.md"

EXACT_JOIN_REPAIR_CSV = RUN_DIR / "exact_join_gap_repair_ledger.csv"
EXACT_JOIN_PREVIEW_CSV = RUN_DIR / "exact_join_gap_repaired_join_preview.csv"
PROXY_REJECTION_CSV = RUN_DIR / "proxy_bridge_rejection_matrix.csv"
PROXY_REBUILD_SPEC_CSV = RUN_DIR / "branch_specific_proxy_rebuild_spec.csv"
CONSTRAINTS_CSV = RUN_DIR / "predeclared_research_constraints.csv"
PACKAGE_MANIFEST_CSV = RUN_DIR / "balanced_repair_defense_offense_input_packages.csv"
DEFENSE_CONTRACT_CSV = RUN_DIR / "defense_guardrail_contract.csv"
OFFENSE_SEED_CSV = RUN_DIR / "offense_research_seed_manifest.csv"
RUN335Q_QUEUE_CSV = RUN_DIR / "run335Q_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_balanced_repair_defense_offense_inputs_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return io_path(path).resolve().relative_to(io_path(ROOT).resolve()).as_posix()


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value is None:
            return default
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return default
    return int(number)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_text_bom(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    next_marker = "\n## "
    section = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find(next_marker, start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + section
        else:
            text = text[:start].rstrip() + "\n\n" + section + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + section
    write_text_lossless(path, text, had_bom)


def read_csv(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(io_path(path))


def load_sources() -> dict[str, pd.DataFrame]:
    return {
        "handoff": read_csv(RUN335K_DIR / "independent_handoff_attempt_manifest.csv"),
        "join": read_csv(RUN335N_DIR / "trade_telemetry_join_audit.csv"),
        "trade": read_csv(RUN335N_DIR / "runtime_trade_ledger.csv"),
        "scorecard": read_csv(RUN335O_DIR / "attempt_runtime_usability_scorecard.csv"),
        "proxy": read_csv(RUN335O_DIR / "proxy_mt5_usability_decision.csv"),
        "repair_queue": read_csv(RUN335O_DIR / "repair_research_queue.csv"),
        "defense_queue": read_csv(RUN335O_DIR / "defensive_guard_queue.csv"),
        "offense_queue": read_csv(RUN335O_DIR / "offensive_research_queue.csv"),
        "fragility": read_csv(RUN335O_DIR / "runtime_fragility_findings.csv"),
    }


def same_minute_floor_key(value: Any) -> str:
    text = str(value)
    if len(text) >= 19 and text.endswith(":01"):
        return text[:-2] + "00"
    return text


def feature_and_telemetry_keys(attempt: str, sources: Mapping[str, pd.DataFrame]) -> tuple[set[str], set[str]]:
    handoff = sources["handoff"]
    handoff_row = handoff[handoff["attempt_name"].eq(attempt)]
    if handoff_row.empty:
        return set(), set()
    feature_path = ROOT / str(handoff_row.iloc[0].get("new_feature_path", ""))
    feature_keys: set[str] = set()
    telemetry_keys: set[str] = set()
    if path_exists(feature_path):
        feature = pd.read_csv(io_path(feature_path), usecols=["bar_time_server"])
        feature_keys = set(feature["bar_time_server"].astype(str))
    telemetry_path = RUN335K_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"
    if path_exists(telemetry_path):
        telemetry = pd.read_csv(io_path(telemetry_path), usecols=["record_type", "bar_time"])
        telemetry = telemetry[telemetry["record_type"].eq("cycle")]
        telemetry_keys = set(telemetry["bar_time"].astype(str))
    return feature_keys, telemetry_keys


def build_exact_join_repair(sources: Mapping[str, pd.DataFrame]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    join = sources["join"]
    missing = join[(join["open_join_status"].ne("matched")) | (join["feature_join_status"].ne("matched"))].copy()
    trade = sources["trade"]
    trade_index = {(str(row["attempt_name"]), str(row["trade_index"])): row for row in trade.to_dict("records")}
    ledger_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    key_cache: dict[str, tuple[set[str], set[str]]] = {}
    for row in missing.to_dict("records"):
        attempt = str(row.get("attempt_name"))
        trade_id = str(row.get("trade_index"))
        open_time = str(row.get("open_time_server"))
        floor_key = same_minute_floor_key(open_time)
        if attempt not in key_cache:
            key_cache[attempt] = feature_and_telemetry_keys(attempt, sources)
        feature_keys, telemetry_keys = key_cache[attempt]
        feature_floor = floor_key in feature_keys
        telemetry_floor = floor_key in telemetry_keys
        can_repair = open_time.endswith(":01") and feature_floor and telemetry_floor
        repair_status = "same_bar_second_floor_attribution_repair_ready" if can_repair else "unresolved_exact_join_gap"
        trade_row = trade_index.get((attempt, trade_id), {})
        ledger_rows.append(
            {
                "attempt_name": attempt,
                "trade_index": trade_id,
                "open_time_server_original": open_time,
                "open_time_server_repair_key": floor_key,
                "close_time_server": row.get("close_time_server", ""),
                "open_join_status_original": row.get("open_join_status", ""),
                "feature_join_status_original": row.get("feature_join_status", ""),
                "repair_status": repair_status,
                "feature_floor_key_exists": str(feature_floor).lower(),
                "telemetry_floor_key_exists": str(telemetry_floor).lower(),
                "repair_scope": "attribution_join_key_only_no_trade_time_mutation",
                "lookahead_risk": "none_if_same_bar_floor_only;blocked_if_future_or_nearest_shift_required",
                "direction": trade_row.get("direction", ""),
                "net_profit": trade_row.get("net_profit", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        preview_rows.append(
            {
                "attempt_name": attempt,
                "trade_index": trade_id,
                "join_key_before": open_time,
                "join_key_after": floor_key if can_repair else "",
                "repair_preview_status": "would_match_feature_and_telemetry" if can_repair else "no_preview_match",
                "allowed_use": "diagnostic_attribution_only",
                "forbidden_use": "model_training_threshold_tuning_lot_optimization_forward_pass_fail_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return ledger_rows, preview_rows


def build_proxy_tables(sources: Mapping[str, pd.DataFrame]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    proxy = sources["proxy"]
    rejection_rows: list[dict[str, Any]] = []
    rebuild_rows: list[dict[str, Any]] = []
    for row in proxy.to_dict("records"):
        dimension = str(row.get("dimension"))
        decision = str(row.get("proxy_usability_decision"))
        numeric_rows = as_int(row.get("numeric_comparable_rows"))
        unique_values = as_int(row.get("unique_proxy_expected_values"))
        is_overall = dimension == "overall_proxy_bridge"
        reject_reason = "overall_proxy_not_selection_usable" if is_overall else decision
        rejection_rows.append(
            {
                "dimension": dimension,
                "numeric_comparable_rows": numeric_rows,
                "unique_proxy_expected_values": unique_values,
                "proxy_usability_decision": decision,
                "selection_use": "blocked",
                "forward_pass_fail_use": "blocked",
                "diagnostic_use": "allowed_context_only",
                "rejection_reason": reject_reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if not is_overall:
            rebuild_rows.append(
                {
                    "dimension": dimension,
                    "required_grain": "branch_id_attempt_name_bar_time_trade_index",
                    "required_inputs": "feature_rows;runtime_decision_rows;trade_ledger;cost_model;predeclared_direction_rules",
                    "must_vary_by": "branch_id;attempt_name",
                    "minimum_checks": "row_count;timestamp_exact_or_same_bar_floor;proxy_vs_mt5_rank_correlation;sign_agreement;negative_control",
                    "anti_overfit_guard": "must_be_defined_before_scoring_new_model_or_threshold;must_not_be_fit_to_run335N_mt5_profit",
                    "materialization_status": "spec_ready_not_built",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rejection_rows, rebuild_rows


def build_constraints(sources: Mapping[str, pd.DataFrame], exact_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    scorecard = sources["scorecard"]
    fragility = sources["fragility"]
    score_by_attempt = {str(row["attempt_name"]): row for row in scorecard.to_dict("records")}
    best = score_by_attempt.get("m48_plain_rf", {})
    cost_fail_05 = int((pd.to_numeric(scorecard["cost_plus_0_5_net"], errors="coerce") <= 0).sum())
    cost_fail_10 = int((pd.to_numeric(scorecard["cost_plus_1_0_net"], errors="coerce") <= 0).sum())
    short_drag = int((pd.to_numeric(scorecard["short_net_profit"], errors="coerce") <= 0).sum())
    high_underwater = int((pd.to_numeric(scorecard["underwater_trade_share"], errors="coerce") > 0.75).sum())
    exact_ready = sum(1 for row in exact_rows if row.get("repair_status") == "same_bar_second_floor_attribution_repair_ready")
    constraints = [
        {
            "constraint_id": "predeclare_cost_buffer_gate",
            "lane": "repair_and_defense",
            "source_finding": "cost_fragility",
            "observed_evidence": f"{cost_fail_05}/6 fail cost_plus_0_5;{cost_fail_10}/6 fail cost_plus_1_0",
            "predeclared_rule": "future research packets must report cost_plus_0_25/0_5/1_0/2_0 before any selection read",
            "allowed_use": "guardrail_kpi_and_failure_memory",
            "forbidden_use": "tune_lot_or_threshold_until_forward_cost_passes",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "predeclare_curve_underwater_gate",
            "lane": "repair_and_defense",
            "source_finding": "curve_underwater_stretch",
            "observed_evidence": f"{high_underwater}/6 attempts underwater_share_gt_0_75",
            "predeclared_rule": "future packets must report rolling5/10/20/50 worst pocket and underwater stretch; no direct calendar pocket filter",
            "allowed_use": "curve_quality_guardrail",
            "forbidden_use": "drop_or_keep_trades_based_on_known_forward_pocket_dates",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "predeclare_direction_symmetry_gate",
            "lane": "offense_and_defense",
            "source_finding": "direction_asymmetry",
            "observed_evidence": f"{short_drag}/6 attempts have non_positive_short_net",
            "predeclared_rule": "future research must show long/short attribution and side-specific failure before side routing changes",
            "allowed_use": "side_reliability_research_seed",
            "forbidden_use": "drop_shorts_only_because_run335N_short_side_lost",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "predeclare_proxy_selection_block",
            "lane": "defense",
            "source_finding": "proxy_repeated_aggregate_context_only",
            "observed_evidence": "proxy dimensions are repeated aggregate values, not branch-specific rank evidence",
            "predeclared_rule": "proxy cannot rank branches until rebuilt at branch/attempt/bar/trade grain",
            "allowed_use": "context_only_diagnostic",
            "forbidden_use": "Forward_Passed_Failed_or_selection_decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "predeclare_exact_join_repair_gate",
            "lane": "repair",
            "source_finding": "exact_join_gap",
            "observed_evidence": f"{exact_ready}/9 trade-level gaps repair-ready by same-bar :01 to :00 floor",
            "predeclared_rule": "same-bar second floor may be used for attribution only; nearest/future shift remains blocked",
            "allowed_use": "attribution_join_repair",
            "forbidden_use": "mutate_trade_time_or_retrain_features",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "predeclare_best_clue_seed_boundary",
            "lane": "offense",
            "source_finding": "m48_plain_rf_best_research_clue",
            "observed_evidence": f"net={best.get('net_profit','')};pf={best.get('profit_factor','')};tpd={best.get('trades_per_calendar_day','')};score={best.get('usability_score','')}",
            "predeclared_rule": "best clue can seed feature-family research, but cannot be selected or promoted",
            "allowed_use": "research_seed",
            "forbidden_use": "candidate_selection_or_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    if fragility.empty:
        constraints.append(
            {
                "constraint_id": "fragility_source_missing",
                "lane": "data_integrity",
                "source_finding": "missing",
                "observed_evidence": "run335O fragility findings missing",
                "predeclared_rule": "run335Q must block review if fragility source remains missing",
                "allowed_use": "blocked_review_condition",
                "forbidden_use": "silent_approval",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return constraints


def build_packages(
    sources: Mapping[str, pd.DataFrame],
    constraints: Sequence[Mapping[str, Any]],
    exact_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    repair_queue = sources["repair_queue"].to_dict("records")
    defense_queue = sources["defense_queue"].to_dict("records")
    offense_queue = sources["offense_queue"].to_dict("records")
    constraint_ids_by_lane: dict[str, list[str]] = {}
    for row in constraints:
        lane = str(row.get("lane", ""))
        constraint_ids_by_lane.setdefault(lane, []).append(str(row.get("constraint_id")))
    packages = [
        {
            "package_id": "run335P_repair_exact_join_and_proxy_bridge",
            "package_lane": "repair",
            "source_queue_ids": ";".join(str(row.get("queue_id")) for row in repair_queue),
            "artifact_inputs": f"{rel(EXACT_JOIN_REPAIR_CSV)};{rel(PROXY_REJECTION_CSV)};{rel(PROXY_REBUILD_SPEC_CSV)}",
            "predeclared_constraints": ";".join(constraint_ids_by_lane.get("repair", []) + constraint_ids_by_lane.get("repair_and_defense", [])),
            "review_status": "ready_for_run335Q_review",
            "selection_eligible": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": "run335P_defense_no_leakage_guardrails",
            "package_lane": "defense",
            "source_queue_ids": ";".join(str(row.get("queue_id")) for row in defense_queue),
            "artifact_inputs": f"{rel(DEFENSE_CONTRACT_CSV)};{rel(PROXY_REJECTION_CSV)};{rel(CONSTRAINTS_CSV)}",
            "predeclared_constraints": ";".join(constraint_ids_by_lane.get("defense", []) + constraint_ids_by_lane.get("offense_and_defense", [])),
            "review_status": "ready_for_run335Q_review",
            "selection_eligible": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "package_id": "run335P_offense_m48_plain_side_cost_seed",
            "package_lane": "offense",
            "source_queue_ids": ";".join(str(row.get("queue_id")) for row in offense_queue),
            "artifact_inputs": f"{rel(OFFENSE_SEED_CSV)};{rel(CONSTRAINTS_CSV)}",
            "predeclared_constraints": ";".join(constraint_ids_by_lane.get("offense", []) + constraint_ids_by_lane.get("offense_and_defense", [])),
            "review_status": "ready_for_run335Q_review",
            "selection_eligible": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    defense_contract = [
        {
            "guard_id": row.get("queue_id"),
            "priority": row.get("priority"),
            "guard_text": row.get("guard"),
            "effect": row.get("effect"),
            "source_evidence": row.get("evidence"),
            "enforcement_point": "run335Q_review_and_future_packet_design",
            "failure_action": "reject_packet_or_mark_blocked_for_repair",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in defense_queue
    ]
    offense_seed = [
        {
            "seed_id": row.get("queue_id"),
            "priority": row.get("priority"),
            "source_attempt": row.get("source_attempt"),
            "seed_action": row.get("action"),
            "seed_reason": row.get("seed_reason"),
            "required_precheck": "cost_curve_direction_proxy_negative_control_gates_must_exist_before_training",
            "forbidden": row.get("forbidden"),
            "selection_eligible": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in offense_queue
    ]
    run335q_queue = [
        {
            "queue_id": "review_exact_join_repair_preview",
            "priority": 1,
            "input_artifact": rel(EXACT_JOIN_REPAIR_CSV),
            "review_task": f"Confirm all repair-ready rows are same-bar second floor only; repair_ready={sum(1 for row in exact_rows if row.get('repair_status') == 'same_bar_second_floor_attribution_repair_ready')}.",
            "pass_condition": "no future or nearest shift required",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_proxy_rebuild_or_block",
            "priority": 2,
            "input_artifact": rel(PROXY_REBUILD_SPEC_CSV),
            "review_task": "Choose whether to build branch-specific proxy at required grain or keep proxy fully blocked for selection.",
            "pass_condition": "proxy ranking stays blocked unless branch-specific grain is materialized",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_predeclared_constraints",
            "priority": 3,
            "input_artifact": rel(CONSTRAINTS_CSV),
            "review_task": "Verify constraints are predeclared research gates, not direct forward-window filters.",
            "pass_condition": "cost/curve/direction/proxy constraints are acceptable for next packet design",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_balanced_packages",
            "priority": 4,
            "input_artifact": rel(PACKAGE_MANIFEST_CSV),
            "review_task": "Check repair, defense, and offense lanes remain balanced and no lane claims selection.",
            "pass_condition": "all packages are review-ready and selection_eligible=false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return packages, defense_contract, offense_seed, run335q_queue


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run335O_queues_loaded",
            "status": "passed",
            "evidence": rel(RUN335O_DIR),
            "finding": f"repair={metrics['repair_queue_rows']};defense={metrics['defense_queue_rows']};offense={metrics['offense_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "exact_join_repair_materialized_without_future_shift",
            "status": "passed" if metrics["exact_join_unresolved"] == 0 else "passed_with_boundary",
            "evidence": rel(EXACT_JOIN_REPAIR_CSV),
            "finding": f"repair_ready={metrics['exact_join_repair_ready']};unresolved={metrics['exact_join_unresolved']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_selection_block_materialized",
            "status": "passed",
            "evidence": rel(PROXY_REJECTION_CSV),
            "finding": "proxy remains diagnostic context only until branch-specific rebuild exists",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "predeclared_constraints_created",
            "status": "passed",
            "evidence": rel(CONSTRAINTS_CSV),
            "finding": f"constraints={metrics['constraint_rows']};no direct forward pocket filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "balanced_packages_created",
            "status": "passed",
            "evidence": rel(PACKAGE_MANIFEST_CSV),
            "finding": f"packages={metrics['package_rows']};selection_eligible=false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_selection_no_goal_achieve",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "no Forward Passed/Failed, no runtime authority, no Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": [rel(RUN335N_DIR), rel(RUN335O_DIR)],
            "time_axis": "MT5 server bar keys; :01 execution opens may floor to the same :00 M5 bar for attribution only.",
            "sample_scope": "run335K/run335N US100 M5 runtime diagnostic window.",
            "missing_or_duplicate_check": f"exact_join_repair_ready={metrics['exact_join_repair_ready']};unresolved={metrics['exact_join_unresolved']}.",
            "feature_label_boundary": "no model training, no threshold retune, no forward pocket filter.",
            "split_boundary": "forward/runtime diagnostic input only.",
            "leakage_risk": "proxy ranking and forward pocket filters remain explicitly blocked.",
            "data_hash_or_identity": "run335P artifacts registered in artifact registry.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(RUN335K_DIR), rel(RUN335N_DIR), rel(RUN335O_DIR)],
            "shared_contract": "same model/threshold/lot/runtime handoff; run335P only materializes review inputs.",
            "known_differences": ":01 open timestamps are same-bar attribution gaps, not runtime decision mismatches.",
            "parity_check": "no new MT5 run; consumes run335L/run335N runtime diagnostic evidence.",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "run335O diagnostic decisions were converted into repair/defense/offense input packages.",
            "comparison_baseline": "previous queue rows were not yet materialized as input artifacts.",
            "likely_drivers": "cost fragility, direction asymmetry, curve underwater stretch, proxy aggregate limitation, exact join gaps.",
            "segment_checks": "exact join; proxy dimensions; cost/curve/direction constraints; offense seed packages.",
            "trade_shape": "m48_plain_rf preserved as research seed only; not selection.",
            "alternative_explanations": "non-identity attempts and aggregate proxy prevent candidate inference.",
            "attribution_confidence": "medium_for_input_design_low_for_selection",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run335P balanced repair defense offense research inputs",
            "evidence_available": "exact join repair ledger, proxy rejection matrix, constraints, packages, queues.",
            "evidence_missing": "run335Q review, branch-specific proxy implementation, new model training, independent MT5 after any repair.",
            "judgment_label": "exploratory_input_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수리·방어·공격 재료는 준비됐지만 후보 선택은 아직 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(RUN335N_DIR), rel(RUN335O_DIR)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(EXACT_JOIN_REPAIR_CSV),
                rel(PROXY_REJECTION_CSV),
                rel(CONSTRAINTS_CSV),
                rel(PACKAGE_MANIFEST_CSV),
                rel(RUN335Q_QUEUE_CSV),
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_stage_closeout",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# Run335P Balanced Repair/Defense/Offense Research Inputs(335P 균형형 수리/방어/공격 연구 입력)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- exact_join_repair_ready(정확 조인 수리 가능): `{metrics['exact_join_repair_ready']}`
- exact_join_unresolved(정확 조인 미해결): `{metrics['exact_join_unresolved']}`
- package_rows(패키지 행): `{metrics['package_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335P(335P 실행)는 run335O(335O 실행)의 repair/defense/offense queue(수리/방어/공격 대기열)를 다음 검토 가능한 연구 입력으로 물질화했다.

Effect(효과): 9개 exact join gap(정확 조인 공백)은 모두 same-bar second floor(동일 봉 초 단위 보정)로 attribution-only repair(귀속 전용 수리) 가능하다. proxy(프록시)는 branch-specific rebuild(분기별 재구축)가 생기기 전까지 selection/Forward decision(선택/전진 판정)에서 차단된다.

## Evidence(근거)

- exact_join_gap_repair_ledger(정확 조인 수리 장부): `{rel(EXACT_JOIN_REPAIR_CSV)}`
- proxy_bridge_rejection_matrix(프록시 차단 행렬): `{rel(PROXY_REJECTION_CSV)}`
- branch_specific_proxy_rebuild_spec(분기별 프록시 재구축 규격): `{rel(PROXY_REBUILD_SPEC_CSV)}`
- predeclared_research_constraints(사전 선언 연구 제약): `{rel(CONSTRAINTS_CSV)}`
- balanced_input_packages(균형 입력 패키지): `{rel(PACKAGE_MANIFEST_CSV)}`
- defense_guardrail_contract(방어 가드레일 계약): `{rel(DEFENSE_CONTRACT_CSV)}`
- offense_research_seed_manifest(공격 연구 씨앗 목록): `{rel(OFFENSE_SEED_CSV)}`
- run335Q_review_queue(335Q 검토 대기열): `{rel(RUN335Q_QUEUE_CSV)}`

## Boundary(경계)

이 실행은 input materialization(입력 물질화)이다. model(모델), threshold(임계값), lot(로트), risk logic(위험 로직), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage335P Balanced Repair/Defense/Offense Inputs(균형형 수리/방어/공격 입력)

`{RUN_ID}`은 run335O(335O 실행)의 다음 작업 대기열을 실제 입력 산출물로 만들었다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- exact_join_repair_ready(정확 조인 수리 가능): `{metrics['exact_join_repair_ready']}`
- exact_join_unresolved(정확 조인 미해결): `{metrics['exact_join_unresolved']}`
- proxy_selection_use(프록시 선택 사용): `blocked`
- package_rows(패키지 행): `{metrics['package_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): 다음 run335Q(335Q 실행)는 이 입력 패키지를 검토해, 수리할 것과 새 연구 패킷으로 넘길 것을 나눌 수 있다.
"""
    write_text_bom(REPORT_DOC, report)
    write_text_bom(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335P(335P 실행)는 "
        f"`{STATUS}`로 balanced repair/defense/offense research inputs(균형형 수리/방어/공격 연구 입력)을 물질화했다. "
        f"Effect(효과): exact join repair-ready(정확 조인 수리 가능) `{metrics['exact_join_repair_ready']}`행, "
        f"package(패키지) `{metrics['package_rows']}`행, run335Q review queue(335Q 검토 대기열) `{metrics['run335q_queue_rows']}`행을 만들고 "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335P(335P 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v17`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run335P_summary(335P 요약): repair/defense/offense research inputs(수리/방어/공격 연구 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): exact join gap(정확 조인 공백)은 same-bar floor(동일 봉 보정)로 귀속 전용 수리 가능하고, proxy(프록시)는 selection(선택)에서 차단하며, "
        f"`{NEXT_RUN_ID}` 검토 대기열로 넘긴다. Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335P_summary(335P 요약)" not in current_text:
        current_text = current_text.replace("- run335O_summary", summary_line + "\n- run335O_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        f"- effect(효과): Stage335P(335P 실행)은 exact join repair(정확 조인 수리), proxy block/rebuild spec(프록시 차단/재구축 규격), cost/curve/direction constraints(비용/곡선/방향 제약), offense seed(공격 씨앗)를 입력 패키지로 만들었다. next_action(다음 행동)은 `{NEXT_RUN_ID}`이며 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- exact_join_gap_repair_ledger(정확 조인 수리 장부): `{rel(EXACT_JOIN_REPAIR_CSV)}`
- proxy_bridge_rejection_matrix(프록시 차단 행렬): `{rel(PROXY_REJECTION_CSV)}`
- branch_specific_proxy_rebuild_spec(분기별 프록시 재구축 규격): `{rel(PROXY_REBUILD_SPEC_CSV)}`
- predeclared_research_constraints(사전 선언 연구 제약): `{rel(CONSTRAINTS_CSV)}`
- balanced_input_packages(균형 입력 패키지): `{rel(PACKAGE_MANIFEST_CSV)}`
- run335Q_review_queue(335Q 검토 대기열): `{rel(RUN335Q_QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335P Balanced Repair Defense Offense Inputs(335P 균형형 수리 방어 공격 입력)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): exact join repair(정확 조인 수리), proxy block/rebuild spec(프록시 차단/재구축 규격), constraints(제약), balanced packages(균형 패키지)를 만들었다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335P Balanced Repair Defense Offense Inputs(335P 균형형 수리 방어 공격 입력)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_balanced_repair_defense_offense_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__balanced_repair_defense_offense_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "balanced_repair_defense_offense_input_materialization",
                "tier_scope": "Tier A runtime diagnostic evidence with no selection",
                "kpi_scope": "exact_join_proxy_cost_curve_direction_package_inputs",
                "scoreboard_lane": "research_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"exact_join_repair_ready={metrics['exact_join_repair_ready']};packages={metrics['package_rows']}",
                "guardrail_kpi": "proxy_selection_blocked;no_forward_pocket_filter;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_input_materialization_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__balanced_repair_defense_offense_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "research_input_materialization",
                "evidence_scope": "run335N_structured_runtime_metrics_run335O_queues",
                "kpi_scope": "repair_defense_offense_input_contracts",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"exact_join_repair_ready={metrics['exact_join_repair_ready']};next={NEXT_RUN_ID}.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_balanced_repair_defense_offense_input_materialization",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "balanced_input_output_no_retune_no_forward_decision",
        }
        for path in outputs
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    exact_rows, preview_rows = build_exact_join_repair(sources)
    proxy_rejection_rows, proxy_rebuild_rows = build_proxy_tables(sources)
    constraints = build_constraints(sources, exact_rows)
    packages, defense_contract, offense_seed, run335q_queue = build_packages(sources, constraints, exact_rows)
    metrics = {
        "repair_queue_rows": len(sources["repair_queue"]),
        "defense_queue_rows": len(sources["defense_queue"]),
        "offense_queue_rows": len(sources["offense_queue"]),
        "exact_join_rows": len(exact_rows),
        "exact_join_repair_ready": sum(1 for row in exact_rows if row.get("repair_status") == "same_bar_second_floor_attribution_repair_ready"),
        "exact_join_unresolved": sum(1 for row in exact_rows if row.get("repair_status") != "same_bar_second_floor_attribution_repair_ready"),
        "proxy_rejection_rows": len(proxy_rejection_rows),
        "proxy_rebuild_rows": len(proxy_rebuild_rows),
        "constraint_rows": len(constraints),
        "package_rows": len(packages),
        "run335q_queue_rows": len(run335q_queue),
    }
    gate_rows = build_gate_rows(metrics)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "exact_join_repair;proxy_rejection;proxy_rebuild_spec;predeclared_constraints;balanced_packages;run335Q_queue",
            "evidence_missing": "run335Q_review;branch_specific_proxy_implementation;new_model;new_mt5_after_any_future_repair",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    outputs = [
        write_csv(
            EXACT_JOIN_REPAIR_CSV,
            (
                "attempt_name",
                "trade_index",
                "open_time_server_original",
                "open_time_server_repair_key",
                "close_time_server",
                "open_join_status_original",
                "feature_join_status_original",
                "repair_status",
                "feature_floor_key_exists",
                "telemetry_floor_key_exists",
                "repair_scope",
                "lookahead_risk",
                "direction",
                "net_profit",
                "claim_boundary",
            ),
            exact_rows,
        ),
        write_csv(
            EXACT_JOIN_PREVIEW_CSV,
            (
                "attempt_name",
                "trade_index",
                "join_key_before",
                "join_key_after",
                "repair_preview_status",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            preview_rows,
        ),
        write_csv(
            PROXY_REJECTION_CSV,
            (
                "dimension",
                "numeric_comparable_rows",
                "unique_proxy_expected_values",
                "proxy_usability_decision",
                "selection_use",
                "forward_pass_fail_use",
                "diagnostic_use",
                "rejection_reason",
                "claim_boundary",
            ),
            proxy_rejection_rows,
        ),
        write_csv(
            PROXY_REBUILD_SPEC_CSV,
            (
                "dimension",
                "required_grain",
                "required_inputs",
                "must_vary_by",
                "minimum_checks",
                "anti_overfit_guard",
                "materialization_status",
                "claim_boundary",
            ),
            proxy_rebuild_rows,
        ),
        write_csv(
            CONSTRAINTS_CSV,
            (
                "constraint_id",
                "lane",
                "source_finding",
                "observed_evidence",
                "predeclared_rule",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            constraints,
        ),
        write_csv(
            PACKAGE_MANIFEST_CSV,
            (
                "package_id",
                "package_lane",
                "source_queue_ids",
                "artifact_inputs",
                "predeclared_constraints",
                "review_status",
                "selection_eligible",
                "claim_boundary",
            ),
            packages,
        ),
        write_csv(
            DEFENSE_CONTRACT_CSV,
            (
                "guard_id",
                "priority",
                "guard_text",
                "effect",
                "source_evidence",
                "enforcement_point",
                "failure_action",
                "claim_boundary",
            ),
            defense_contract,
        ),
        write_csv(
            OFFENSE_SEED_CSV,
            (
                "seed_id",
                "priority",
                "source_attempt",
                "seed_action",
                "seed_reason",
                "required_precheck",
                "forbidden",
                "selection_eligible",
                "claim_boundary",
            ),
            offense_seed,
        ),
        write_csv(
            RUN335Q_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "input_artifact",
                "review_task",
                "pass_condition",
                "claim_boundary",
            ),
            run335q_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), gate_rows),
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        ),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "metrics": metrics,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(RUN335N_DIR), rel(RUN335O_DIR)],
                "status": STATUS,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    write_reports(metrics)
    outputs.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    outputs.extend([WORKSPACE_STATE, CURRENT_STATE, STAGE_BRIEF, INPUT_REFS, CHANGELOG, SELECTED_DIR / "selection_status.md"])
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "exact_join_repair_ready": metrics["exact_join_repair_ready"],
                "exact_join_unresolved": metrics["exact_join_unresolved"],
                "package_rows": metrics["package_rows"],
                "run335q_queue_rows": metrics["run335q_queue_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
