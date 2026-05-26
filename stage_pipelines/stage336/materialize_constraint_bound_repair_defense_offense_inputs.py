from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336B"
RUN_ID = "run336B_materialize_constraint_bound_repair_defense_offense_inputs_v1"
PARENT_RUN_ID = "run336A_design_constraint_bound_repair_defense_offense_rebuild_packet_v1"
NEXT_RUN_ID = "run336C_review_constraint_bound_materialized_inputs_v1"

STATUS = "completed_constraint_bound_repair_defense_offense_inputs_materialized_no_selection"
JUDGMENT = "materialized_repair_defense_offense_runtime_inputs_proxy_blocked_no_selection"
DECISION = "stage336B_materialized_constraint_bound_inputs_ready_for_review_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336B_constraint_bound_input_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336A_DIR = STAGE_DIR / "02_runs" / "run336A"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage336B_constraint_bound_input_materialization.md"
REPORT_DOC = REVIEWS_DIR / "run336B_constraint_bound_input_materialization.md"

BRANCH_DESIGN_CSV = RUN336A_DIR / "constraint_bound_rebuild_branch_design_matrix.csv"
PROXY_CONTRACT_CSV = RUN336A_DIR / "predeclared_scoring_and_proxy_exclusion_contract.csv"
GATE_CONTRACT_CSV = RUN336A_DIR / "cost_curve_direction_gate_contract.csv"
RUNTIME_CONTRACT_CSV = RUN336A_DIR / "runtime_parity_probe_contract.csv"
NEGATIVE_CONTROL_CSV = RUN336A_DIR / "negative_control_and_stop_condition_matrix.csv"
RUN336B_QUEUE_CSV = RUN336A_DIR / "run336B_materialization_queue.csv"

BRANCH_SPEC_CARDS_CSV = RUN_DIR / "branch_spec_cards.csv"
PROXY_BLOCK_MANIFEST_CSV = RUN_DIR / "score_input_allowlist_and_proxy_block_manifest.csv"
GATE_TEMPLATE_MANIFEST_CSV = RUN_DIR / "gate_template_manifest.csv"
RUNTIME_PREFLIGHT_SCHEMA_CSV = RUN_DIR / "runtime_parity_preflight_schema.csv"
NEGATIVE_CONTROL_CHECKLIST_CSV = RUN_DIR / "negative_control_checklist.csv"
REGIME_SLICE_SCHEMA_CSV = RUN_DIR / "regime_slice_output_schema.csv"
PACKAGE_MANIFEST_CSV = RUN_DIR / "materialized_input_package_manifest.csv"
RUN336C_REVIEW_QUEUE_CSV = RUN_DIR / "run336C_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_constraint_bound_input_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

REGIME_SLICES = (
    ("session", "ny_session_bucket", "predeclare cash/open/mid/close/off-session buckets without using forward result"),
    ("hour", "broker_hour_and_ny_hour", "report every hour; no after-result profitable hour filter"),
    ("month", "calendar_month", "report month only for attribution; do not drop known weak calendar pocket"),
    ("volatility", "atr_hv_quantile", "use predeclared quantile labels from training/reference window only"),
    ("ADX", "adx_strength_bucket", "weak/medium/strong trend buckets must be reported for all branches"),
    ("VIX", "vix_level_or_change_bucket", "risk proxy slice must remain diagnostic until fresh MT5 comparison"),
    ("USD", "usdx_change_or_zscore_bucket", "USD regime must not be selected after seeing branch PnL"),
    ("rate", "us10yr_change_or_zscore_bucket", "rate regime must remain attribution only unless separately validated"),
)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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
        newline="\n",
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


def insert_after_once(text: str, anchor: str, marker: str, body: str) -> str:
    if marker in text:
        return text
    index = text.find(anchor)
    if index == -1:
        return text.rstrip() + "\n" + body.strip() + "\n"
    insertion = index + len(anchor)
    return text[:insertion] + body + text[insertion:]


def append_once(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    if header in text:
        return
    write_text_lossless(path, text.rstrip() + "\n\n" + header + "\n\n" + body.strip() + "\n", had_bom)


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "branches": read_csv(BRANCH_DESIGN_CSV),
        "proxy_contract": read_csv(PROXY_CONTRACT_CSV),
        "gate_contract": read_csv(GATE_CONTRACT_CSV),
        "runtime_contract": read_csv(RUNTIME_CONTRACT_CSV),
        "negative_controls": read_csv(NEGATIVE_CONTROL_CSV),
        "queue": read_csv(RUN336B_QUEUE_CSV),
    }


def build_branch_spec_cards(branches: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, branch in enumerate(branches, start=1):
        branch_id = branch["branch_id"]
        rows.append(
            {
                "package_id": f"run336B_pkg_{index:02d}_{branch_id}",
                "branch_id": branch_id,
                "lane": branch["lane"],
                "branch_role": branch["branch_role"],
                "seed_or_clue": branch["seed_or_clue"],
                "source_constraints": branch["source_constraints"],
                "materialized_inputs": branch["materialization_action"],
                "required_outputs": branch["required_outputs"],
                "required_gate_bundle": "run336B_gate_template_bundle_v1",
                "proxy_policy_id": "run336B_proxy_block_manifest_v1",
                "runtime_policy_id": "run336B_runtime_preflight_schema_v1",
                "negative_controls": branch["negative_controls"],
                "stop_conditions": branch["stop_conditions"],
                "review_ready": "true",
                "selection_eligible": "false",
                "forbidden_actions": "model_training;threshold_retuning;lot_optimization;candidate_selection;direct_forward_pocket_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_block_manifest(
    branches: Sequence[Mapping[str, str]],
    proxy_contract: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branches:
        for item in proxy_contract:
            dimension = item["dimension"]
            rows.append(
                {
                    "manifest_id": f"{branch['branch_id']}__{item['contract_id']}",
                    "branch_id": branch["branch_id"],
                    "dimension": dimension,
                    "rank_use": "blocked" if item["rank_use"] == "blocked" else "predeclared_only_after_review",
                    "forward_decision_use": "blocked",
                    "diagnostic_use": item["diagnostic_use"],
                    "old_proxy_value_allowed": "false",
                    "required_rebuild_grain": item["required_rebuild_grain"],
                    "acceptance_evidence": item["acceptance_evidence"],
                    "score_input_allowlist": "predeclared_feature_family_only;fresh_branch_grain_metric_after_review",
                    "forbidden_use": item["forbidden_use"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_gate_template_manifest(
    branches: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branches:
        for gate in gates:
            rows.append(
                {
                    "template_id": f"{branch['branch_id']}__{gate['gate_id']}",
                    "branch_id": branch["branch_id"],
                    "lane": branch["lane"],
                    "gate_id": gate["gate_id"],
                    "required_measurement": gate["required_measurement"],
                    "output_table_name": f"{branch['branch_id']}__{gate['gate_id']}_table",
                    "review_requirement": gate["acceptance_boundary"],
                    "failure_memory_trigger": gate["failure_memory_trigger"],
                    "forbidden_shortcut": gate["forbidden_shortcut"],
                    "review_ready": "true",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_runtime_preflight_schema(
    branches: Sequence[Mapping[str, str]],
    runtime_contract: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branches:
        for contract in runtime_contract:
            rows.append(
                {
                    "schema_id": f"{branch['branch_id']}__{contract['contract_id']}",
                    "branch_id": branch["branch_id"],
                    "runtime_subject": contract["runtime_subject"],
                    "required_identity": contract["required_identity"],
                    "required_check": contract["required_check"],
                    "acceptance_evidence": contract["acceptance_evidence"],
                    "external_verification_status": "out_of_scope_by_claim_materialization_only",
                    "preflight_status": "schema_materialized_no_runtime_execution",
                    "forbidden": contract["forbidden"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_negative_control_checklist(
    branches: Sequence[Mapping[str, str]],
    controls: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    branch_control_map = {
        branch["branch_id"]: set(split_semicolon(branch.get("negative_controls", ""))) for branch in branches
    }
    for branch in branches:
        explicit_controls = branch_control_map[branch["branch_id"]]
        for control in controls:
            control_id = control["control_id"]
            rows.append(
                {
                    "check_id": f"{branch['branch_id']}__{control_id}",
                    "branch_id": branch["branch_id"],
                    "control_id": control_id,
                    "target_risk": control["target_risk"],
                    "enforcement_scope": "explicit_branch_control" if control_id in explicit_controls else "global_required_control",
                    "test_design": control["test_design"],
                    "expected_failure_signature": control["expected_failure_signature"],
                    "stop_condition": control["stop_condition"],
                    "repair_action": control["repair_action"],
                    "enforcement_status": "predeclared_required",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_regime_slice_schema(branches: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in branches:
        for slice_id, field_name, rule in REGIME_SLICES:
            rows.append(
                {
                    "schema_id": f"{branch['branch_id']}__{slice_id}",
                    "branch_id": branch["branch_id"],
                    "slice_id": slice_id,
                    "output_field": field_name,
                    "bucket_policy": rule,
                    "required_metrics": "trade_count;net_profit;profit_factor;expectancy;max_drawdown;recovery_factor;time_under_water;long_short_split",
                    "allowed_use": "attribution_and_failure_memory_only_until_independent_validation",
                    "forbidden_use": "pick_profitable_slice_after_result;direct_forward_pocket_filter",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_package_manifest(branch_spec_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "branch_id": row["branch_id"],
            "lane": row["lane"],
            "branch_spec_card": rel(BRANCH_SPEC_CARDS_CSV),
            "proxy_block_manifest": rel(PROXY_BLOCK_MANIFEST_CSV),
            "gate_template_manifest": rel(GATE_TEMPLATE_MANIFEST_CSV),
            "runtime_preflight_schema": rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
            "negative_control_checklist": rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
            "regime_slice_schema": rel(REGIME_SLICE_SCHEMA_CSV),
            "review_queue": rel(RUN336C_REVIEW_QUEUE_CSV),
            "materialization_status": "materialized_ready_for_review",
            "selected_candidate": "none",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in branch_spec_rows
    ]


def build_run336c_queue(branch_spec_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue = [
        {
            "queue_id": "review_branch_spec_card_completeness",
            "priority": 1,
            "source_artifact": rel(BRANCH_SPEC_CARDS_CSV),
            "task": "Review every branch spec card for source constraints, required outputs, controls, and forbidden actions.",
            "success_condition": "all branch cards remain selection-ineligible and review-ready",
            "forbidden": "candidate_selection;model_training_before_review",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_proxy_block_manifest",
            "priority": 2,
            "source_artifact": rel(PROXY_BLOCK_MANIFEST_CSV),
            "task": "Verify old proxy values are blocked from rank and Forward decision paths.",
            "success_condition": "rank_use and forward_decision_use stay blocked for old proxy rows",
            "forbidden": "proxy_rank_use;retrofit_proxy_to_mt5_profit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_gate_template_coverage",
            "priority": 3,
            "source_artifact": rel(GATE_TEMPLATE_MANIFEST_CSV),
            "task": "Verify each branch has cost, curve, underwater, direction, regime, and lot-normalized gate templates.",
            "success_condition": "branch_count times gate_count coverage is complete",
            "forbidden": "skip_gate_after_good_kpi;direct_forward_pocket_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_runtime_preflight_schema",
            "priority": 4,
            "source_artifact": rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
            "task": "Verify runtime preflight requires feature/model/report/telemetry/row-level parity identity.",
            "success_condition": "future MT5 runtime probe cannot claim authority without tester and telemetry evidence",
            "forbidden": "runtime_authority_without_tester_output",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_negative_control_enforcement",
            "priority": 5,
            "source_artifact": rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
            "task": "Verify lookahead, proxy, threshold, lot, side, regime, and runtime authority controls are enforceable.",
            "success_condition": "each branch carries all global controls and explicit branch controls",
            "forbidden": "skip_negative_control_after_good_kpi",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_regime_slice_schema",
            "priority": 6,
            "source_artifact": rel(REGIME_SLICE_SCHEMA_CSV),
            "task": "Verify session, hour, month, volatility, ADX, VIX, USD, and rate slices are attribution-only.",
            "success_condition": "regime slices cannot become after-result branch filters",
            "forbidden": "pick_profitable_slice_after_result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in branch_spec_rows:
        queue.append(
            {
                "queue_id": f"review_package_{row['branch_id']}",
                "priority": 10,
                "source_artifact": rel(PACKAGE_MANIFEST_CSV),
                "task": f"Review materialized package for {row['branch_id']}.",
                "success_condition": "package can move to controlled research implementation only after review passes",
                "forbidden": "candidate_selection;Forward_Passed;runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return queue


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected_proxy_rows = metrics["branch_rows"] * metrics["proxy_contract_input_rows"]
    expected_gate_rows = metrics["branch_rows"] * metrics["gate_input_rows"]
    expected_runtime_rows = metrics["branch_rows"] * metrics["runtime_input_rows"]
    expected_control_rows = metrics["branch_rows"] * metrics["negative_control_input_rows"]
    expected_regime_rows = metrics["branch_rows"] * len(REGIME_SLICES)
    return [
        {
            "gate_id": "run336A_inputs_loaded",
            "status": "passed" if metrics["queue_input_rows"] == 6 and metrics["branch_rows"] == 6 else "failed",
            "evidence": rel(RUN336B_QUEUE_CSV),
            "finding": f"queue_input_rows={metrics['queue_input_rows']};branch_rows={metrics['branch_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_spec_cards_materialized",
            "status": "passed" if metrics["branch_spec_rows"] == metrics["branch_rows"] else "failed",
            "evidence": rel(BRANCH_SPEC_CARDS_CSV),
            "finding": f"branch_spec_rows={metrics['branch_spec_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_block_manifest_complete",
            "status": "passed" if metrics["proxy_block_rows"] == expected_proxy_rows and metrics["proxy_rank_allowed_rows"] == 0 else "failed",
            "evidence": rel(PROXY_BLOCK_MANIFEST_CSV),
            "finding": f"proxy_block_rows={metrics['proxy_block_rows']};expected={expected_proxy_rows};rank_allowed_rows={metrics['proxy_rank_allowed_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate_templates_complete",
            "status": "passed" if metrics["gate_template_rows"] == expected_gate_rows else "failed",
            "evidence": rel(GATE_TEMPLATE_MANIFEST_CSV),
            "finding": f"gate_template_rows={metrics['gate_template_rows']};expected={expected_gate_rows}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_preflight_complete",
            "status": "passed" if metrics["runtime_preflight_rows"] == expected_runtime_rows else "failed",
            "evidence": rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
            "finding": f"runtime_preflight_rows={metrics['runtime_preflight_rows']};expected={expected_runtime_rows}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_controls_complete",
            "status": "passed" if metrics["negative_check_rows"] == expected_control_rows else "failed",
            "evidence": rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
            "finding": f"negative_check_rows={metrics['negative_check_rows']};expected={expected_control_rows}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "regime_slice_schema_complete",
            "status": "passed" if metrics["regime_schema_rows"] == expected_regime_rows else "failed",
            "evidence": rel(REGIME_SLICE_SCHEMA_CSV),
            "finding": f"regime_schema_rows={metrics['regime_schema_rows']};expected={expected_regime_rows}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "selected candidate, Forward Passed/Failed, runtime authority, live readiness, deployment, operating promotion, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    receipts = {
        "data_integrity_receipt.json": {
            "run_id": RUN_ID,
            "data_source": [
                rel(BRANCH_DESIGN_CSV),
                rel(PROXY_CONTRACT_CSV),
                rel(GATE_CONTRACT_CSV),
                rel(RUNTIME_CONTRACT_CSV),
                rel(NEGATIVE_CONTROL_CSV),
            ],
            "time_axis": "No new bar data is created; future branches must preserve FPMarkets broker-clock and closed-bar contracts.",
            "sample_scope": "Stage336B materializes research inputs only; no train/validation/OOS KPI is generated.",
            "missing_or_duplicate_check": f"branch_packages={metrics['package_rows']};gate_templates={metrics['gate_template_rows']};runtime_preflight_rows={metrics['runtime_preflight_rows']}",
            "feature_label_boundary": "Feature families and regime slices are predeclared before future results; no labels, model, or thresholds are computed.",
            "split_boundary": "future Tier A/Tier B and MT5 runtime records are required but not produced in this materialization run.",
            "leakage_risk": "old proxy rank use, forward pocket filtering, after-result feature picking, and future timestamp repair remain explicit stop conditions.",
            "data_hash_or_identity": {
                "branch_design": sha256_file_lf_normalized(BRANCH_DESIGN_CSV),
                "proxy_contract": sha256_file_lf_normalized(PROXY_CONTRACT_CSV),
                "gate_contract": sha256_file_lf_normalized(GATE_CONTRACT_CSV),
                "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_CSV),
            },
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt.json": {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(RUNTIME_PREFLIGHT_SCHEMA_CSV)],
            "shared_contract": "future runtime probes must carry feature order, model bundle, MT5 report, telemetry, row-level parity, and external verification status.",
            "known_differences": "run336B materializes preflight schema only and does not execute MT5.",
            "parity_check": "runtime preflight schema materialized; external verification status is out_of_scope_by_claim_materialization_only.",
            "parity_identity": {"runtime_preflight_rows": metrics["runtime_preflight_rows"], "next_run": NEXT_RUN_ID},
            "runtime_claim_boundary": "research_only_materialized_preflight_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "performance_attribution_receipt.json": {
            "run_id": RUN_ID,
            "observed_change": "run336A design became branch packages, gate templates, proxy blocks, runtime preflight, controls, and regime slice schema.",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "materialized guardrails around proxy misuse, cost/curve fragility, side attribution, regime overfit, and runtime parity.",
            "segment_checks": "session, hour, month, volatility, ADX, VIX, USD, rate slices are predeclared for future branch outputs.",
            "trade_shape": "no new trades; future branch packages require trade count, expectancy, DD, underwater, and long/short splits.",
            "alternative_explanations": "input completeness does not prove signal quality or forward robustness.",
            "attribution_confidence": "medium_for_materialization_only",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "artifact_lineage_receipt.json": {
            "run_id": RUN_ID,
            "source_inputs": [rel(RUN336A_DIR)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(BRANCH_SPEC_CARDS_CSV),
                rel(PROXY_BLOCK_MANIFEST_CSV),
                rel(GATE_TEMPLATE_MANIFEST_CSV),
                rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
                rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
                rel(REGIME_SLICE_SCHEMA_CSV),
                rel(PACKAGE_MANIFEST_CSV),
                rel(RUN336C_REVIEW_QUEUE_CSV),
            ],
            "artifact_hashes": "registered in docs/registers/artifact_registry.csv",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_run_artifacts",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt.json": {
            "run_id": RUN_ID,
            "result_subject": "Stage336B constraint-bound input materialization",
            "evidence_available": "branch packages, proxy block manifest, gate templates, runtime preflight, negative controls, regime slice schema, review queue",
            "evidence_missing": "review of materialized inputs, new model training, fresh MT5 runtime probe, selected candidate, Forward Passed/Failed evidence",
            "judgment_label": "exploratory",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "이번 실행은 설계를 실제 다음 연구 입력으로 바꿨지만 아직 후보나 성과 판정은 아니다.",
        },
    }
    return [write_json(RUN_DIR / name, payload) for name, payload in receipts.items()]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# Stage336B Constraint-Bound Input Materialization(336B단계 제약 기반 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## What Materialized(물질화 내용)

run336A(336A 실행)의 design(설계)을 실제 review-ready inputs(검토 준비 입력)로 바꿨다.
효과(effect, 효과)는 다음 run336C(336C 실행)가 후보를 고르기 전에 proxy(프록시), gate(게이트), runtime parity(런타임 동등성), negative control(부정 대조)을 먼저 검토하게 하는 것이다.

## Counts(개수)

- branch spec cards(분기 명세 카드): `{metrics['branch_spec_rows']}` rows(행)
- proxy block manifest(프록시 차단 목록): `{metrics['proxy_block_rows']}` rows(행)
- gate templates(게이트 틀): `{metrics['gate_template_rows']}` rows(행)
- runtime preflight schema(런타임 사전 점검 구조): `{metrics['runtime_preflight_rows']}` rows(행)
- negative-control checklist(부정 대조 체크리스트): `{metrics['negative_check_rows']}` rows(행)
- regime slice schema(국면 조각 구조): `{metrics['regime_schema_rows']}` rows(행)
- package manifest(패키지 목록): `{metrics['package_rows']}` rows(행)

## Boundary(경계)

This is materialization only(물질화 전용)이다.
Model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision_doc = f"""
# Stage336B Decision(336B단계 결정): Constraint-Bound Input Materialization(제약 기반 입력 물질화)

- decision(결정): `{DECISION}`
- result_subject(판정 대상): Stage336B materialized repair/defense/offense/runtime inputs(수리/방어/공격/런타임 입력 물질화)
- evidence_available(사용 근거): branch spec cards(분기 명세 카드), proxy block manifest(프록시 차단 목록), gate templates(게이트 틀), runtime preflight schema(런타임 사전 점검 구조), negative-control checklist(부정 대조 체크리스트), regime slice schema(국면 조각 구조)
- evidence_missing(부족 근거): input review(입력 검토), model training(모델 학습), MT5 runtime probe(MT5 런타임 탐침), selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패)
- judgment_label(판정 라벨): `exploratory`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

효과(effect, 효과): 다음 실행은 materialized inputs(물질화 입력)을 검토한 뒤에야 실제 연구 구현으로 넘어갈 수 있다. Proxy(프록시)는 rank(순위)와 Forward decision(전진 판정)에 계속 차단된다.

Boundary(경계): `{CLAIM_BOUNDARY}`
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision_doc)]


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_body = (
        "  Stage336(336단계) run336B(336B 실행)는 "
        f"`{STATUS}`로 constraint-bound materialized inputs(제약 기반 물질화 입력)을 만들었다. "
        f"Effect(효과): branch packages(분기 패키지) `{metrics['package_rows']}`개, "
        f"gate templates(게이트 틀) `{metrics['gate_template_rows']}`개, "
        f"runtime preflight rows(런타임 사전 점검 행) `{metrics['runtime_preflight_rows']}`개를 만들고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_once(
        workspace_text,
        "current_focus:\n",
        "run336B(336B 실행)",
        f"- >-\n{focus_body}\n",
    )
    write_text_lossless(WORKSPACE_STATE, workspace_text.rstrip() + "\n", workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary = (
        f"- run336B_summary(336B 요약): constraint-bound materialized inputs(제약 기반 물질화 입력)을 "
        f"`{STATUS}`로 만들었다. Effect(효과): branch spec cards(분기 명세 카드) `{metrics['branch_spec_rows']}`행, "
        f"proxy block manifest(프록시 차단 목록) `{metrics['proxy_block_rows']}`행, "
        f"negative-control checklist(부정 대조 체크리스트) `{metrics['negative_check_rows']}`행을 만들고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    current_text = insert_after_once(
        current_text,
        f"- decision(결정): `{DECISION}`\n",
        "run336B_summary(336B 요약)",
        summary,
    )
    write_text_lossless(CURRENT_STATE, current_text.rstrip() + "\n", current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): Stage336(336단계)는 run336B(336B 실행)에서 수리/방어/공격/런타임 입력을 물질화했으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text.rstrip() + "\n", selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text.rstrip() + "\n", brief_bom)

    input_refs_path = INPUTS_DIR / "input_refs.md"
    input_refs_text, input_refs_bom = read_text_lossless(input_refs_path)
    section = f"""

## run336B Outputs(336B 산출물)

- branch_spec_cards(분기 명세 카드): `{rel(BRANCH_SPEC_CARDS_CSV)}`
- proxy_block_manifest(프록시 차단 목록): `{rel(PROXY_BLOCK_MANIFEST_CSV)}`
- gate_template_manifest(게이트 틀 목록): `{rel(GATE_TEMPLATE_MANIFEST_CSV)}`
- runtime_preflight_schema(런타임 사전 점검 구조): `{rel(RUNTIME_PREFLIGHT_SCHEMA_CSV)}`
- negative_control_checklist(부정 대조 체크리스트): `{rel(NEGATIVE_CONTROL_CHECKLIST_CSV)}`
- regime_slice_schema(국면 조각 구조): `{rel(REGIME_SLICE_SCHEMA_CSV)}`
- package_manifest(패키지 목록): `{rel(PACKAGE_MANIFEST_CSV)}`
- run336C_review_queue(336C 검토 대기열): `{rel(RUN336C_REVIEW_QUEUE_CSV)}`
"""
    input_refs_text = insert_after_once(
        input_refs_text,
        "Boundary(경계): 이 입력은 research design(연구 설계)용이며 selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 만들지 않는다.\n",
        "run336B Outputs(336B 산출물)",
        section,
    )
    write_text_lossless(input_refs_path, input_refs_text.rstrip() + "\n", input_refs_bom)

    append_once(
        CHANGELOG,
        "## 2026-05-26 Stage336B Constraint-Bound Input Materialization(336B 제약 기반 입력 물질화)",
        f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): branch package(분기 패키지), proxy block(프록시 차단), gate template(게이트 틀), runtime preflight(런타임 사전 점검), negative control(부정 대조), regime slice(국면 조각) 입력을 만들었다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
""",
    )


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_constraint_bound_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};packages={metrics['package_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__materialized_inputs",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "constraint_bound_input_materialization",
            "tier_scope": "paired_tier_required_by_future_contract",
            "kpi_scope": "materialization_only_no_new_trading_kpi",
            "scoreboard_lane": "experiment_execution",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_DOC),
            "primary_kpi": f"packages={metrics['package_rows']};branch_spec_rows={metrics['branch_spec_rows']}",
            "guardrail_kpi": f"proxy_rank_allowed_rows={metrics['proxy_rank_allowed_rows']};negative_checks={metrics['negative_check_rows']}",
            "external_verification_status": "out_of_scope_by_claim_materialization_only",
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__proxy_runtime_gate_controls",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "proxy_runtime_gate_controls",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "proxy_runtime_gate_materialization",
            "tier_scope": "paired_tier_required_by_future_contract",
            "kpi_scope": "guardrail_manifest_no_trading_kpi",
            "scoreboard_lane": "defense_runtime",
            "status": STATUS,
            "judgment": "proxy_runtime_gate_controls_materialized",
            "path": rel(PROXY_BLOCK_MANIFEST_CSV),
            "primary_kpi": f"proxy_block_rows={metrics['proxy_block_rows']};runtime_preflight_rows={metrics['runtime_preflight_rows']}",
            "guardrail_kpi": f"gate_template_rows={metrics['gate_template_rows']};regime_schema_rows={metrics['regime_schema_rows']}",
            "external_verification_status": "out_of_scope_by_claim_materialization_only",
            "notes": "proxy_rank_blocked;runtime_authority_not_claimed.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
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
                "ledger_row_id": f"{RUN_ID}__constraint_bound_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "constraint_bound_repair_defense_offense_input_materialization",
                "evidence_scope": "run336A_design_to_run336B_materialized_inputs",
                "kpi_scope": "materialization_only_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"packages={metrics['package_rows']};gate_templates={metrics['gate_template_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    created = now_utc()
    artifact_rows = []
    for path in outputs:
        if not path_exists(path):
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336B_constraint_bound_input_materialization",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336B_materialization_no_selection_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    inputs = load_inputs()
    branch_spec_rows = build_branch_spec_cards(inputs["branches"])
    proxy_block_rows = build_proxy_block_manifest(inputs["branches"], inputs["proxy_contract"])
    gate_template_rows = build_gate_template_manifest(inputs["branches"], inputs["gate_contract"])
    runtime_preflight_rows = build_runtime_preflight_schema(inputs["branches"], inputs["runtime_contract"])
    negative_check_rows = build_negative_control_checklist(inputs["branches"], inputs["negative_controls"])
    regime_schema_rows = build_regime_slice_schema(inputs["branches"])
    package_rows = build_package_manifest(branch_spec_rows)
    review_queue_rows = build_run336c_queue(branch_spec_rows)

    metrics = {
        "queue_input_rows": len(inputs["queue"]),
        "branch_rows": len(inputs["branches"]),
        "proxy_contract_input_rows": len(inputs["proxy_contract"]),
        "gate_input_rows": len(inputs["gate_contract"]),
        "runtime_input_rows": len(inputs["runtime_contract"]),
        "negative_control_input_rows": len(inputs["negative_controls"]),
        "branch_spec_rows": len(branch_spec_rows),
        "proxy_block_rows": len(proxy_block_rows),
        "proxy_rank_allowed_rows": sum(1 for row in proxy_block_rows if row["rank_use"] not in {"blocked", "predeclared_only_after_review"}),
        "gate_template_rows": len(gate_template_rows),
        "runtime_preflight_rows": len(runtime_preflight_rows),
        "negative_check_rows": len(negative_check_rows),
        "regime_schema_rows": len(regime_schema_rows),
        "package_rows": len(package_rows),
        "run336c_queue_rows": len(review_queue_rows),
    }
    gate_rows = build_gate_audit(metrics)
    failed_gates = [row["gate_id"] for row in gate_rows if row["status"] != "passed"]
    result_status = STATUS if not failed_gates else "blocked_stage336B_gate_failure"
    result_judgment = JUDGMENT if not failed_gates else "stage336B_materialization_gate_failure_requires_repair"
    result_decision = DECISION if not failed_gates else "stage336B_materialization_blocked_gate_failure"

    outputs = [
        write_csv(
            BRANCH_SPEC_CARDS_CSV,
            (
                "package_id",
                "branch_id",
                "lane",
                "branch_role",
                "seed_or_clue",
                "source_constraints",
                "materialized_inputs",
                "required_outputs",
                "required_gate_bundle",
                "proxy_policy_id",
                "runtime_policy_id",
                "negative_controls",
                "stop_conditions",
                "review_ready",
                "selection_eligible",
                "forbidden_actions",
                "claim_boundary",
            ),
            branch_spec_rows,
        ),
        write_csv(
            PROXY_BLOCK_MANIFEST_CSV,
            (
                "manifest_id",
                "branch_id",
                "dimension",
                "rank_use",
                "forward_decision_use",
                "diagnostic_use",
                "old_proxy_value_allowed",
                "required_rebuild_grain",
                "acceptance_evidence",
                "score_input_allowlist",
                "forbidden_use",
                "claim_boundary",
            ),
            proxy_block_rows,
        ),
        write_csv(
            GATE_TEMPLATE_MANIFEST_CSV,
            (
                "template_id",
                "branch_id",
                "lane",
                "gate_id",
                "required_measurement",
                "output_table_name",
                "review_requirement",
                "failure_memory_trigger",
                "forbidden_shortcut",
                "review_ready",
                "claim_boundary",
            ),
            gate_template_rows,
        ),
        write_csv(
            RUNTIME_PREFLIGHT_SCHEMA_CSV,
            (
                "schema_id",
                "branch_id",
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "external_verification_status",
                "preflight_status",
                "forbidden",
                "claim_boundary",
            ),
            runtime_preflight_rows,
        ),
        write_csv(
            NEGATIVE_CONTROL_CHECKLIST_CSV,
            (
                "check_id",
                "branch_id",
                "control_id",
                "target_risk",
                "enforcement_scope",
                "test_design",
                "expected_failure_signature",
                "stop_condition",
                "repair_action",
                "enforcement_status",
                "claim_boundary",
            ),
            negative_check_rows,
        ),
        write_csv(
            REGIME_SLICE_SCHEMA_CSV,
            (
                "schema_id",
                "branch_id",
                "slice_id",
                "output_field",
                "bucket_policy",
                "required_metrics",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            regime_schema_rows,
        ),
        write_csv(
            PACKAGE_MANIFEST_CSV,
            (
                "package_id",
                "branch_id",
                "lane",
                "branch_spec_card",
                "proxy_block_manifest",
                "gate_template_manifest",
                "runtime_preflight_schema",
                "negative_control_checklist",
                "regime_slice_schema",
                "review_queue",
                "materialization_status",
                "selected_candidate",
                "claim_boundary",
            ),
            package_rows,
        ),
        write_csv(
            RUN336C_REVIEW_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            review_queue_rows,
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
                "judgment_label",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            [
                {
                    "run_id": RUN_ID,
                    "status": result_status,
                    "judgment": result_judgment,
                    "decision": result_decision,
                    "evidence_available": "branch_spec_cards;proxy_block_manifest;gate_templates;runtime_preflight_schema;negative_control_checklist;regime_slice_schema;package_manifest;review_queue",
                    "evidence_missing": "run336C review;model training;fresh MT5 runtime probe;selected candidate;Forward Passed/Failed evidence",
                    "judgment_label": "exploratory" if not failed_gates else "blocked",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        ),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": result_status,
                "judgment": result_judgment,
                "decision": result_decision,
                "metrics": metrics,
                "failed_gates": failed_gates,
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
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": [
                    rel(BRANCH_DESIGN_CSV),
                    rel(PROXY_CONTRACT_CSV),
                    rel(GATE_CONTRACT_CSV),
                    rel(RUNTIME_CONTRACT_CSV),
                    rel(NEGATIVE_CONTROL_CSV),
                    rel(RUN336B_QUEUE_CSV),
                ],
                "status": result_status,
                "decision": result_decision,
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    outputs.extend(write_reports(metrics))
    if failed_gates:
        print(json.dumps({"run_id": RUN_ID, "failed_gates": failed_gates}, ensure_ascii=False, indent=2))
        return 2

    update_docs(metrics)
    outputs.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            SELECTED_DIR / "selection_status.md",
            SPEC_DIR / "stage_brief.md",
            INPUTS_DIR / "input_refs.md",
        ]
    )
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "branch_spec_rows": metrics["branch_spec_rows"],
                "proxy_block_rows": metrics["proxy_block_rows"],
                "gate_template_rows": metrics["gate_template_rows"],
                "runtime_preflight_rows": metrics["runtime_preflight_rows"],
                "negative_check_rows": metrics["negative_check_rows"],
                "regime_schema_rows": metrics["regime_schema_rows"],
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
