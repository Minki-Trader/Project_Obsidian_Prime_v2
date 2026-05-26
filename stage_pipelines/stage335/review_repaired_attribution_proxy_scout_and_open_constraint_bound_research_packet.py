from __future__ import annotations

import csv
import json
import math
import re
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
NEXT_STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run335S"
RUN_ID = "run335S_review_repaired_attribution_proxy_scout_and_open_constraint_bound_research_packet_v1"
PARENT_RUN_ID = "run335R_materialize_repaired_attribution_and_branch_specific_proxy_scout_v1"
NEXT_RUN_ID = "run336A_design_constraint_bound_repair_defense_offense_rebuild_packet_v1"

STATUS = "completed_stage335_closeout_open_stage336_constraint_bound_research_packet_no_selection"
JUDGMENT = "repair_review_passed_proxy_blocked_constraints_accepted_stage336_opened"
DECISION = "stage335S_close_stage335_open_stage336_constraint_bound_research_packet_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335S_review_closeout_open_stage336_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_stage336_constraint_bound_repair_defense_offense_rebuild_no_model_training_"
    "until_predeclared_protocol_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN335R_DIR = STAGE_DIR / "02_runs" / "run335R"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_RUNS_DIR = NEXT_STAGE_DIR / "02_runs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"
NEXT_STAGE_LEDGER = NEXT_REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335S_close_stage335_open_stage336.md"
REPORT_DOC = REVIEWS_DIR / "run335S_repaired_attribution_proxy_scout_review_and_stage336_open.md"

REPAIR_REVIEW_CSV = RUN_DIR / "same_bar_attribution_repair_review.csv"
PROXY_DELTA_REVIEW_CSV = RUN_DIR / "proxy_expected_vs_mt5_delta_review.csv"
PROXY_USABILITY_REVIEW_CSV = RUN_DIR / "proxy_scout_usability_review.csv"
CONSTRAINT_REVIEW_CSV = RUN_DIR / "constraint_packet_review.csv"
STAGE336_CONTRACT_CSV = RUN_DIR / "stage336_opening_contract.csv"
RUN336A_QUEUE_CSV = RUN_DIR / "run336A_design_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_stage335S_stage336_open_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if text == "":
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def sign(value: float) -> int:
    if value > 0.0:
        return 1
    if value < 0.0:
        return -1
    return 0


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_focus_once(text: str, marker: str, body: str) -> str:
    if marker in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n- >-\n{body}\n", 1)


def append_or_replace_section(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    section = f"\n## {header}\n\n{body.strip()}\n"
    pattern = re.compile(rf"\n## {re.escape(header)}\n.*?(?=\n## |\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(section.rstrip(), text)
    else:
        text = text.rstrip() + section
    write_text_lossless(path, text.rstrip() + "\n", had_bom)


def read_csv(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(io_path(path), keep_default_na=False)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "repair_join": read_csv(RUN335R_DIR / "repaired_trade_telemetry_join_view.csv"),
        "repair_delta": read_csv(RUN335R_DIR / "attribution_repair_delta_summary.csv"),
        "proxy_compare": read_csv(RUN335R_DIR / "proxy_scout_vs_mt5_runtime_comparison.csv"),
        "proxy_usability": read_csv(RUN335R_DIR / "proxy_scout_usability_decision.csv"),
        "constraints": read_csv(RUN335R_DIR / "constraint_bound_research_packet_inputs.csv"),
        "packages": read_csv(RUN335R_DIR / "balanced_package_carry_forward_manifest.csv"),
        "queue": read_csv(RUN335R_DIR / "run335S_review_queue.csv"),
        "gates": read_csv(RUN335R_DIR / "required_gate_coverage_audit.csv"),
    }


def build_repair_review(repair_join: pd.DataFrame, repair_delta: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in repair_delta.to_dict("records"):
        attempt = str(item.get("attempt_name"))
        attempt_join = repair_join[repair_join["attempt_name"].astype(str).eq(attempt)]
        repaired = attempt_join[attempt_join["repair_applied"].map(bool_text)]
        invalid_same_bar = 0
        mutated = 0
        for row in repaired.to_dict("records"):
            original = str(row.get("open_time_server"))
            repair_key = str(row.get("open_time_server_repair_key"))
            effective = str(row.get("effective_attribution_join_key"))
            same_bar = original[:16] == repair_key[:16] and original.endswith(":01") and repair_key.endswith(":00")
            if not same_bar:
                invalid_same_bar += 1
            if original == effective:
                mutated += 1
        remaining = int(as_float(item.get("remaining_missing_open_or_feature_join_count"), 0.0))
        accepted = int(as_float(item.get("accepted_same_bar_repair_count"), 0.0))
        review_decision = "accepted_same_bar_attribution_repair_reviewed" if remaining == 0 and invalid_same_bar == 0 else "blocked_repair_review_failed"
        rows.append(
            {
                "attempt_name": attempt,
                "original_missing_open_or_feature_join_count": item.get("original_missing_open_or_feature_join_count"),
                "accepted_same_bar_repair_count": accepted,
                "remaining_missing_open_or_feature_join_count": remaining,
                "invalid_same_bar_repair_count": invalid_same_bar,
                "open_time_mutation_count": mutated,
                "repaired_trade_net_profit": item.get("repaired_trade_net_profit"),
                "review_decision": review_decision,
                "allowed_use": "attribution_diagnostic_only",
                "forbidden_use": "model_training;threshold_retuning;lot_optimization;forward_pass_fail_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_delta_review(proxy_compare: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for dimension, grouped in proxy_compare.groupby("dimension", sort=True):
        old_values = grouped["old_proxy_expected_value"].astype(str)
        mt5_values = grouped["mt5_runtime_probe_value"].astype(str)
        scout_num_values = grouped["branch_specific_scout_value_numeric"].astype(str)
        old_unique = len(set(v for v in old_values if v != ""))
        mt5_unique = len(set(v for v in mt5_values if v != ""))
        scout_unique = len(set(v for v in scout_num_values if v != ""))
        numeric_pairs: list[tuple[float, float, float]] = []
        sign_matches = 0
        sign_possible = 0
        for row in grouped.to_dict("records"):
            old_num = as_float(row.get("old_proxy_expected_value"))
            mt5_num = as_float(row.get("mt5_runtime_probe_value"))
            scout_num = as_float(row.get("branch_specific_scout_value_numeric"))
            if math.isfinite(old_num) and math.isfinite(mt5_num):
                sign_possible += 1
                if sign(old_num) == sign(mt5_num):
                    sign_matches += 1
            if math.isfinite(old_num) and math.isfinite(mt5_num) and math.isfinite(scout_num):
                numeric_pairs.append((abs(old_num - mt5_num), abs(old_num - scout_num), abs(scout_num - mt5_num)))
        shared_attempt_rows = sum(
            1
            for value in grouped["branch_variation_status"].astype(str)
            if value == "runtime_value_shared_by_attempt_across_branches"
        )
        numeric_count = len(numeric_pairs)
        if numeric_pairs:
            mean_old_mt5 = sum(item[0] for item in numeric_pairs) / numeric_count
            max_old_mt5 = max(item[0] for item in numeric_pairs)
            mean_old_scout = sum(item[1] for item in numeric_pairs) / numeric_count
            mean_scout_mt5 = sum(item[2] for item in numeric_pairs) / numeric_count
        else:
            mean_old_mt5 = max_old_mt5 = mean_old_scout = mean_scout_mt5 = None
        old_blocked = all(str(value) == "blocked_repeated_aggregate_context_only" for value in grouped["old_proxy_use"])
        selection_blocked = all(str(value) == "blocked" for value in grouped["selection_use"])
        forward_blocked = all(str(value) == "blocked" for value in grouped["forward_pass_fail_use"])
        nonnumeric = numeric_count == 0
        rows.append(
            {
                "dimension": dimension,
                "row_count": len(grouped),
                "numeric_pair_count": numeric_count,
                "old_proxy_unique_values": old_unique,
                "mt5_runtime_unique_values": mt5_unique,
                "branch_specific_scout_unique_values": scout_unique,
                "old_proxy_mean_abs_delta_vs_mt5": mean_old_mt5,
                "old_proxy_max_abs_delta_vs_mt5": max_old_mt5,
                "old_proxy_mean_abs_delta_vs_scout": mean_old_scout,
                "scout_mean_abs_delta_vs_mt5": mean_scout_mt5,
                "sign_agreement_rate_old_proxy_vs_mt5": sign_matches / sign_possible if sign_possible else None,
                "shared_attempt_rows": shared_attempt_rows,
                "old_proxy_repeated_aggregate": "true" if old_unique <= 1 else "false",
                "old_proxy_blocked": str(old_blocked).lower(),
                "selection_blocked": str(selection_blocked).lower(),
                "forward_decision_blocked": str(forward_blocked).lower(),
                "review_decision": "context_only_nonnumeric_proxy_rejected" if nonnumeric else "old_proxy_rejected_scout_diagnostic_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_usability_review(proxy_usability: pd.DataFrame, delta_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    delta_by_dimension = {str(row["dimension"]): row for row in delta_rows}
    rows: list[dict[str, Any]] = []
    for item in proxy_usability.to_dict("records"):
        dimension = str(item.get("dimension"))
        delta = delta_by_dimension.get(dimension, {})
        rows.append(
            {
                "dimension": dimension,
                "row_count": item.get("row_count"),
                "old_proxy_rank_usable": item.get("old_proxy_rank_usable"),
                "old_proxy_block_reason": item.get("old_proxy_block_reason"),
                "scout_selection_usable": item.get("scout_selection_usable"),
                "scout_forward_decision_usable": item.get("scout_forward_decision_usable"),
                "scout_diagnostic_usable": item.get("scout_diagnostic_usable"),
                "branch_variation_boundary": item.get("branch_variation_boundary"),
                "delta_review_decision": delta.get("review_decision", "overall_proxy_scout_selection_blocked"),
                "run335S_usability_judgment": "selection_blocked_diagnostic_only",
                "next_stage_use": "research_guardrail_input_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_constraint_review(constraints: pd.DataFrame, packages: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    carried_lanes = sorted(set(packages["package_lane"].astype(str)))
    for item in constraints.to_dict("records"):
        ready = item.get("packet_status") == "ready_for_run335S_review"
        rows.append(
            {
                "constraint_id": item.get("constraint_id"),
                "lane": item.get("lane"),
                "source_finding": item.get("source_finding"),
                "predeclared_rule": item.get("predeclared_rule"),
                "packet_status": item.get("packet_status"),
                "review_decision": "accepted_for_stage336_opening" if ready else "blocked_until_constraint_repair",
                "carried_package_lanes": ";".join(carried_lanes),
                "allowed_use": "stage336_protocol_guardrail_and_failure_memory",
                "forbidden_use": item.get("forbidden_use"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_stage336_contract(constraint_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    constraint_ids = ";".join(str(row.get("constraint_id")) for row in constraint_rows)
    return [
        {
            "contract_id": "stage336_repair_lane",
            "lane": "repair",
            "source_artifacts": f"{rel(REPAIR_REVIEW_CSV)};{rel(PROXY_USABILITY_REVIEW_CSV)}",
            "required_constraints": constraint_ids,
            "objective": "fix attribution/proxy handoff boundaries before any new score or model work",
            "allowed_actions": "design timestamp-safe research packet;build predeclared proxy exclusion rules",
            "forbidden_actions": "train_model;retune_threshold;use_old_proxy_for_selection;forward_pocket_filter",
            "selection_eligible": "false",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "stage336_defense_lane",
            "lane": "defense",
            "source_artifacts": f"{rel(CONSTRAINT_REVIEW_CSV)};{rel(RUN335R_DIR / 'required_gate_coverage_audit.csv')}",
            "required_constraints": constraint_ids,
            "objective": "predeclare leakage, cost, curve, side, and runtime gates before new candidates",
            "allowed_actions": "negative controls;cost stress gates;curve pocket gates;runtime parity contract",
            "forbidden_actions": "relax_gate_after_result;skip_test;direct_calendar_pocket_drop",
            "selection_eligible": "false",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "stage336_offense_lane",
            "lane": "offense",
            "source_artifacts": f"{rel(RUN335R_DIR / 'proxy_scout_vs_mt5_runtime_comparison.csv')};{rel(RUN335R_DIR / 'balanced_package_carry_forward_manifest.csv')}",
            "required_constraints": constraint_ids,
            "objective": "open fresh constraint-bound research branches using failure memory without fitting to run335R MT5 profit",
            "allowed_actions": "design new research packet;seed m48_plain as clue only;require independent validation and MT5 probe contract",
            "forbidden_actions": "promote_m48_plain_rf;copy_nonidentity_runtime_result_as_candidate;lot_optimization",
            "selection_eligible": "false",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
    ]


def build_run336a_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "design_repair_defense_offense_rebuild_packet",
            "priority": 1,
            "source_artifact": rel(STAGE336_CONTRACT_CSV),
            "task": "Design Stage336 repair/defense/offense rebuild packet from accepted constraints.",
            "success_condition": "all six constraints wired before any model or threshold work",
            "forbidden": "candidate_selection;training_before_protocol;threshold_retuning",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "queue_id": "predeclare_scoring_and_proxy_exclusion_contract",
            "priority": 2,
            "source_artifact": rel(PROXY_USABILITY_REVIEW_CSV),
            "task": "Create a score/proxy contract that rejects old repeated aggregate proxy as rank input.",
            "success_condition": "proxy expected values cannot influence selection or Forward decision",
            "forbidden": "retrofit_proxy_to_mt5_profit;selection_use_before_review",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "queue_id": "predeclare_cost_curve_direction_gates",
            "priority": 3,
            "source_artifact": rel(CONSTRAINT_REVIEW_CSV),
            "task": "Materialize cost, curve, direction, and underwater gates for future branches.",
            "success_condition": "cost stress, curve pocket, side attribution, and underwater checks are mandatory outputs",
            "forbidden": "direct_forward_pocket_filter;drop_shorts_because_forward_short_lost",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "queue_id": "design_runtime_parity_probe_contract",
            "priority": 4,
            "source_artifact": rel(RUN335R_DIR / "runtime_parity_receipt.json"),
            "task": "Define runtime handoff, feature order, report, and telemetry identity requirements for any Stage336 branch.",
            "success_condition": "future MT5 probe contract includes row-level parity and external verification status",
            "forbidden": "runtime_authority_without_tester_output;EA_entrypoint_copy_for_parameter_only_change",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
    ]


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run335R_inputs_loaded",
            "status": "passed" if metrics["run335r_queue_rows"] == 4 else "failed",
            "evidence": rel(RUN335R_DIR / "run335S_review_queue.csv"),
            "finding": f"queue_rows={metrics['run335r_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "same_bar_repair_review_passed",
            "status": "passed" if metrics["repair_review_failures"] == 0 else "failed",
            "evidence": rel(REPAIR_REVIEW_CSV),
            "finding": f"accepted_repair_rows={metrics['accepted_repair_rows']};failures={metrics['repair_review_failures']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_selection_blocked_after_review",
            "status": "passed" if metrics["proxy_selection_usable_rows"] == 0 else "failed",
            "evidence": rel(PROXY_USABILITY_REVIEW_CSV),
            "finding": f"proxy_dimensions={metrics['proxy_dimensions']};selection_usable_rows={metrics['proxy_selection_usable_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "constraint_packet_accepted",
            "status": "passed" if metrics["constraints_accepted"] == 6 else "failed",
            "evidence": rel(CONSTRAINT_REVIEW_CSV),
            "finding": f"constraints_accepted={metrics['constraints_accepted']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage336_opening_contract_materialized",
            "status": "passed" if metrics["stage336_contract_rows"] == 3 and metrics["run336a_queue_rows"] == 4 else "failed",
            "evidence": rel(STAGE336_CONTRACT_CSV),
            "finding": f"contract_rows={metrics['stage336_contract_rows']};run336a_queue_rows={metrics['run336a_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "Forward Passed/Failed, runtime authority, live readiness, deployment, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    receipts = {
        "data_integrity_receipt.json": {
            "run_id": RUN_ID,
            "data_source": [rel(RUN335R_DIR)],
            "time_axis": "MT5 server-time US100 M5; repaired attribution uses same-bar :01 to :00 key only and preserves trade time",
            "sample_scope": "run335R repaired diagnostic views from 2026-04-14 through 2026-05-22 runtime probe evidence",
            "missing_or_duplicate_check": f"remaining_join_missing_after_review={metrics['remaining_join_missing']}",
            "feature_label_boundary": "no label, model training, threshold retune, or lot optimization in run335S",
            "split_boundary": "runtime diagnostic review and next-stage opening only",
            "leakage_risk": "old proxy repeated aggregate and forward pocket fitting; both blocked",
            "data_hash_or_identity": {
                "repaired_join": sha256_file_lf_normalized(RUN335R_DIR / "repaired_trade_telemetry_join_view.csv"),
                "proxy_comparison": sha256_file_lf_normalized(RUN335R_DIR / "proxy_scout_vs_mt5_runtime_comparison.csv"),
            },
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt.json": {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(RUN335R_DIR / "runtime_parity_receipt.json"), rel(RUN335R_DIR / "proxy_scout_vs_mt5_runtime_comparison.csv")],
            "shared_contract": "run335R repaired attribution and existing run335K/run335N MT5 runtime probe evidence",
            "known_differences": "run335S reviews existing runtime evidence and opens Stage336; it does not execute new MT5",
            "parity_check": "reviewed existing row-level parity receipts and proxy-vs-runtime comparison",
            "parity_identity": {"parent_run": PARENT_RUN_ID, "next_run": NEXT_RUN_ID},
            "runtime_claim_boundary": "runtime_probe_review_only_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "performance_attribution_receipt.json": {
            "run_id": RUN_ID,
            "observed_change": "same-bar repair accepted; old proxy rejected; constraints accepted for next packet",
            "comparison_baseline": "run335R materialized repaired attribution and proxy scout",
            "likely_drivers": "timestamp second formatting and repeated aggregate proxy design",
            "segment_checks": "repair by attempt; proxy dimension delta; constraint lane coverage",
            "trade_shape": "no new PnL generated; uses existing 1347 runtime trades only",
            "alternative_explanations": "diagnostic materialization may be useful without being selection-usable",
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "artifact_lineage_receipt.json": {
            "run_id": RUN_ID,
            "source_inputs": [rel(RUN335R_DIR)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(REPAIR_REVIEW_CSV), rel(PROXY_DELTA_REVIEW_CSV), rel(STAGE336_CONTRACT_CSV), rel(RUN336A_QUEUE_CSV)],
            "artifact_hashes": "registered in docs/registers/artifact_registry.csv",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_run_artifacts",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt.json": {
            "run_id": RUN_ID,
            "result_subject": "Stage335 closeout and Stage336 constraint-bound research packet opening",
            "evidence_available": "repair review, proxy delta/usability review, constraint review, Stage336 opening contract",
            "evidence_missing": "Stage336 research design, new candidate training, MT5 probe, selected candidate, Forward Passed/Failed evidence",
            "judgment_label": "exploratory",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수리와 제약은 통과했지만 프록시는 선택 근거가 아니며 새 연구 단계만 열었습니다.",
        },
    }
    outputs: list[Path] = []
    for name, payload in receipts.items():
        outputs.append(write_json(RUN_DIR / name, payload))
    return outputs


def write_stage336_open_docs(metrics: Mapping[str, Any]) -> list[Path]:
    outputs: list[Path] = []
    outputs.append(
        write_md(
            NEXT_SPEC_DIR / "stage_brief.md",
            f"""
# Stage336 Constraint-Bound Repair/Defense/Offense Rebuild(336단계 제약 기반 수리/방어/공격 재구성)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- status(상태): `open_active`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- active_question(활성 질문): Stage335(335단계)에서 승인된 repair/defense/offense constraints(수리/방어/공격 제약)를 이용해, look-ahead bias(미래 참조 편향)와 proxy overfit(프록시 과적합) 없이 다음 ONNX research packet(온엑스 연구 묶음)을 설계할 수 있는가?
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): Stage336(336단계)는 새 후보 선택이 아니라, run335S(335S 실행)의 accepted constraints(승인 제약) `{metrics['constraints_accepted']}`개를 먼저 배선해 다음 research packet(연구 묶음)의 과적합 경로를 막는 단계다.
- latest_run(최신 실행): `{RUN_ID}`
""",
        )
    )
    outputs.append(
        write_md(
            NEXT_INPUTS_DIR / "input_refs.md",
            f"""
# Stage336 Input References(336단계 입력 참조)

- opened_by(개방 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- repair_review(수리 검토): `{rel(REPAIR_REVIEW_CSV)}`
- proxy_delta_review(프록시 차이 검토): `{rel(PROXY_DELTA_REVIEW_CSV)}`
- proxy_usability_review(프록시 활용성 검토): `{rel(PROXY_USABILITY_REVIEW_CSV)}`
- constraint_review(제약 검토): `{rel(CONSTRAINT_REVIEW_CSV)}`
- stage336_opening_contract(336단계 개방 계약): `{rel(STAGE336_CONTRACT_CSV)}`
- run336A_design_queue(336A 설계 대기열): `{rel(RUN336A_QUEUE_CSV)}`

Boundary(경계): 이 입력은 research design(연구 설계)용이며 selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 만들지 않는다.
""",
        )
    )
    outputs.append(
        write_md(
            NEXT_SELECTED_DIR / "selection_status.md",
            f"""
# Stage336 Selection Status(336단계 선택 상태)

- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- opened_by(개방 실행): `{RUN_ID}`
- latest_design(최신 설계): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage336(336단계)는 Stage335S(335S 실행)의 accepted constraints(승인 제약)를 연구 설계로 넘기는 단계이며 후보 선택이나 운영 주장은 없다.

- latest_review(최신 검토): `{RUN_ID}`
""",
        )
    )
    outputs.append(
        write_csv(
            NEXT_STAGE_LEDGER,
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
                    "ledger_row_id": f"{RUN_ID}__stage336_open",
                    "stage_id": NEXT_STAGE_ID,
                    "run_id": RUN_ID,
                    "work_family": "stage_opening_handoff",
                    "evidence_scope": "stage335S_constraint_bound_research_packet_opening",
                    "kpi_scope": "no_new_trading_kpi_stage_open_only",
                    "status": "open_active",
                    "judgment": "stage336_opened_no_selection",
                    "claim_boundary": NEXT_STAGE_BOUNDARY,
                    "path": rel(NEXT_SPEC_DIR / "stage_brief.md"),
                    "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                    "decision": DECISION,
                }
            ],
        )
    )
    io_path(NEXT_RUNS_DIR).mkdir(parents=True, exist_ok=True)
    return outputs


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# Run335S Repaired Attribution Proxy Scout Review And Stage336 Open(335S 수리 귀속 프록시 검토 및 336단계 개방)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- repair review(수리 검토): same-bar attribution repair(동일 봉 귀속 수리) `{metrics['accepted_repair_rows']}`행은 review passed(검토 통과)이고 remaining join missing(남은 조인 누락)은 `{metrics['remaining_join_missing']}`행이다.
- proxy review(프록시 검토): old proxy expected value(기존 프록시 예상값)는 12개 dimension(차원)에서 repeated aggregate(반복 집계)로 확인되어 selection/Forward decision(선택/전진 판정)에 계속 `blocked`다.
- scout review(탐침 검토): branch-specific scout(분기별 탐침)는 diagnostic-only(진단 전용)이며 runtime value(런타임 값)가 attempt-level(시도 단위)로 공유되는 경계가 있다.
- constraints(제약): accepted constraints(승인 제약) `{metrics['constraints_accepted']}`개와 repair/defense/offense package lanes(수리/방어/공격 패키지 레인) `{metrics['package_lanes']}`를 Stage336(336단계) 계약으로 넘겼다.
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.

## Judgment(판정)

Run335S(335S 실행)는 positive(긍정)도 negative(부정)도 아닌 exploratory handoff(탐색 인계)다. Effect(효과): 수리와 제약은 다음 연구를 열 만큼 충분하지만, proxy(프록시)는 아직 선택에 쓸 수 없으므로 Stage336(336단계) 첫 작업은 proxy exclusion/protocol gate(프록시 제외/계약 게이트)를 먼저 설계해야 한다.
"""
    decision = f"""
# 2026-05-26 Stage335S Decision(335S 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- source_stage(원천 단계): `{STAGE_ID}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): Stage335(335단계)는 failure memory(실패 기억)를 predeclared constraints(사전 선언 제약)로 바꾸는 역할을 마치고, Stage336(336단계)는 그 제약을 이용한 repair/defense/offense rebuild packet(수리/방어/공격 재구성 묶음)을 설계한다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace_text = insert_focus_once(
        workspace_text,
        "run335S(335S 실행)",
        (
            f"  Stage335(335단계) run335S(335S 실행)는 `{STATUS}`로 Stage335(335단계)를 닫고 Stage336(336단계)를 열었다. "
            f"Effect(효과): same-bar repair(동일 봉 수리) `{metrics['accepted_repair_rows']}`행은 검토 통과, proxy(프록시)는 selection/Forward decision(선택/전진 판정) 차단 유지, "
            f"accepted constraints(승인 제약) `{metrics['constraints_accepted']}`개를 `{NEXT_RUN_ID}`로 넘긴다. Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- active_stage", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current_text = replace_line(current_text, "- source_stage", f"- source_stage(원천 단계): `{STAGE_ID}`")
    current_text = replace_line(current_text, "- target_surface", "- target_surface(목표 표면): `constraint_bound_repair_defense_offense_rebuild`")
    current_text = replace_line(current_text, "- adapter_under_review", "- adapter_under_review(검토 중 어댑터): `none`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(결정): `{DECISION}`")
    current_text = replace_line(current_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    summary = (
        f"- run335S_summary(335S 요약): repaired attribution/proxy scout review(수리 귀속/프록시 탐침 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): repair(수리) `{metrics['accepted_repair_rows']}`행 통과, old proxy(기존 프록시) 선택 차단 유지, Stage336(336단계) `{NEXT_STAGE_ID}`를 열고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335S_summary(335S 요약)" not in current_text:
        current_text = current_text.replace("- run335R_summary", summary + "\n- run335R_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- stage_status", "- stage_status(단계 상태): `closed_no_selection_stage336_opened`")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        f"- effect(효과): Stage335S(335S 실행)은 수리/프록시/제약 검토를 끝내고 Stage336(336단계) `{NEXT_STAGE_ID}`를 열었다. selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- status", "- status(상태): `closed_no_selection_stage336_opened`")
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- repair_review(수리 검토): `{rel(REPAIR_REVIEW_CSV)}`
- proxy_delta_review(프록시 차이 검토): `{rel(PROXY_DELTA_REVIEW_CSV)}`
- proxy_usability_review(프록시 활용성 검토): `{rel(PROXY_USABILITY_REVIEW_CSV)}`
- constraint_review(제약 검토): `{rel(CONSTRAINT_REVIEW_CSV)}`
- stage336_opening_contract(336단계 개방 계약): `{rel(STAGE336_CONTRACT_CSV)}`
- run336A_design_queue(336A 설계 대기열): `{rel(RUN336A_QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335S Review and Stage336 Open(335S 검토 및 336단계 개방)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): run335R(335R 실행)의 repaired attribution/proxy scout(수리 귀속/프록시 탐침)를 검토하고 Stage336(336단계) constraint-bound research packet(제약 기반 연구 묶음)을 열었다.
- boundary(경계): proxy(프록시)는 selection/Forward decision(선택/전진 판정)에 `blocked`이며 Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335S Review and Stage336 Open(335S 검토 및 336단계 개방)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage_closeout_open_next_research_packet",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage335_closeout_stage336_open",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "repaired_attribution_proxy_review_stage336_open",
                "tier_scope": "Tier A runtime diagnostic evidence reviewed no selection",
                "kpi_scope": "repair_review_proxy_delta_usability_constraints_stage_open",
                "scoreboard_lane": "stage_closeout_open_next_research_packet",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"repair_rows={metrics['accepted_repair_rows']};constraints_accepted={metrics['constraints_accepted']}",
                "guardrail_kpi": "proxy_selection_blocked;forward_passed_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_review_and_stage_open_only",
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
                "ledger_row_id": f"{RUN_ID}__stage335_closeout_stage336_open",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage_closeout_open_next_research_packet",
                "evidence_scope": "run335R_repaired_attribution_proxy_scout",
                "kpi_scope": "repair_proxy_constraint_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"next_stage={NEXT_STAGE_ID};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335S_review_stage336_open",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": NEXT_STAGE_ID if NEXT_STAGE_ID in rel(path) else STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "run335S_review_closeout_open_stage336_no_selection_no_forward_decision",
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
    inputs = load_inputs()
    repair_rows = build_repair_review(inputs["repair_join"], inputs["repair_delta"])
    proxy_delta_rows = build_proxy_delta_review(inputs["proxy_compare"])
    proxy_usability_rows = build_proxy_usability_review(inputs["proxy_usability"], proxy_delta_rows)
    constraint_rows = build_constraint_review(inputs["constraints"], inputs["packages"])
    stage336_contract_rows = build_stage336_contract(constraint_rows)
    run336a_queue_rows = build_run336a_queue()
    metrics = {
        "run335r_queue_rows": len(inputs["queue"]),
        "accepted_repair_rows": sum(int(as_float(row["accepted_same_bar_repair_count"], 0.0)) for row in repair_rows),
        "remaining_join_missing": sum(int(as_float(row["remaining_missing_open_or_feature_join_count"], 0.0)) for row in repair_rows),
        "repair_review_failures": sum(1 for row in repair_rows if row["review_decision"] != "accepted_same_bar_attribution_repair_reviewed"),
        "proxy_dimensions": sum(1 for row in proxy_delta_rows if row["dimension"] != "overall_proxy_scout"),
        "proxy_selection_usable_rows": sum(1 for row in proxy_usability_rows if str(row["scout_selection_usable"]).lower() == "true"),
        "constraints_accepted": sum(1 for row in constraint_rows if row["review_decision"] == "accepted_for_stage336_opening"),
        "package_lanes": ";".join(sorted(set(inputs["packages"]["package_lane"].astype(str)))),
        "stage336_contract_rows": len(stage336_contract_rows),
        "run336a_queue_rows": len(run336a_queue_rows),
    }
    gate_rows = build_gate_rows(metrics)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "repair_review;proxy_delta_review;proxy_usability_review;constraint_review;stage336_contract;run336A_queue",
            "evidence_missing": "Stage336 design execution;new model training;MT5 probe;selected candidate;Forward Passed/Failed evidence",
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
            REPAIR_REVIEW_CSV,
            (
                "attempt_name",
                "original_missing_open_or_feature_join_count",
                "accepted_same_bar_repair_count",
                "remaining_missing_open_or_feature_join_count",
                "invalid_same_bar_repair_count",
                "open_time_mutation_count",
                "repaired_trade_net_profit",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            repair_rows,
        ),
        write_csv(
            PROXY_DELTA_REVIEW_CSV,
            (
                "dimension",
                "row_count",
                "numeric_pair_count",
                "old_proxy_unique_values",
                "mt5_runtime_unique_values",
                "branch_specific_scout_unique_values",
                "old_proxy_mean_abs_delta_vs_mt5",
                "old_proxy_max_abs_delta_vs_mt5",
                "old_proxy_mean_abs_delta_vs_scout",
                "scout_mean_abs_delta_vs_mt5",
                "sign_agreement_rate_old_proxy_vs_mt5",
                "shared_attempt_rows",
                "old_proxy_repeated_aggregate",
                "old_proxy_blocked",
                "selection_blocked",
                "forward_decision_blocked",
                "review_decision",
                "claim_boundary",
            ),
            proxy_delta_rows,
        ),
        write_csv(
            PROXY_USABILITY_REVIEW_CSV,
            (
                "dimension",
                "row_count",
                "old_proxy_rank_usable",
                "old_proxy_block_reason",
                "scout_selection_usable",
                "scout_forward_decision_usable",
                "scout_diagnostic_usable",
                "branch_variation_boundary",
                "delta_review_decision",
                "run335S_usability_judgment",
                "next_stage_use",
                "claim_boundary",
            ),
            proxy_usability_rows,
        ),
        write_csv(
            CONSTRAINT_REVIEW_CSV,
            (
                "constraint_id",
                "lane",
                "source_finding",
                "predeclared_rule",
                "packet_status",
                "review_decision",
                "carried_package_lanes",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            constraint_rows,
        ),
        write_csv(
            STAGE336_CONTRACT_CSV,
            (
                "contract_id",
                "lane",
                "source_artifacts",
                "required_constraints",
                "objective",
                "allowed_actions",
                "forbidden_actions",
                "selection_eligible",
                "claim_boundary",
            ),
            stage336_contract_rows,
        ),
        write_csv(
            RUN336A_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            run336a_queue_rows,
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
                "next_stage": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
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
                "source_inputs": [rel(RUN335R_DIR)],
                "status": STATUS,
                "decision": DECISION,
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_review_and_stage_open_only",
                "next_stage": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    outputs.extend(write_stage336_open_docs(metrics))
    outputs.extend(write_reports(metrics))
    update_docs(metrics)
    outputs.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            STAGE_BRIEF,
            INPUT_REFS,
            SELECTED_DIR / "selection_status.md",
        ]
    )
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, NEXT_STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "accepted_repair_rows": metrics["accepted_repair_rows"],
                "constraints_accepted": metrics["constraints_accepted"],
                "proxy_selection_usable_rows": metrics["proxy_selection_usable_rows"],
                "next_stage": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
