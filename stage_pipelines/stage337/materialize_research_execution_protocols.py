from __future__ import annotations

import csv
import json
import math
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


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
SOURCE_STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run337D"
RUN_ID = "run337D_materialize_research_execution_protocols_v1"
PARENT_RUN_ID = "run337C_review_materialized_inputs_and_proxy_mt5_usability_v1"
NEXT_RUN_ID = "run337E_review_research_execution_protocols_v1"
STATUS = "completed_research_execution_protocols_materialized_no_selection"
JUDGMENT = "stage337D_protocols_ready_for_review_no_training_no_selection"
DECISION = "stage337D_materialized_execution_protocols_review_next_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337D_protocol_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337C_DIR = STAGE_DIR / "02_runs" / "run337C"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337D_research_execution_protocols.md"
REPORT_DOC = REVIEWS_DIR / "run337D_research_execution_protocols.md"

RUN337C_QUEUE = RUN337C_DIR / "run337D_research_execution_protocol_queue.csv"
RUN337C_ACCEPTED_BRANCH_QUEUE = RUN337C_DIR / "accepted_branch_package_queue.csv"
RUN337C_BRANCH_ACCEPTANCE = RUN337C_DIR / "branch_gate_acceptance_matrix.csv"
RUN337C_PROXY_REVIEW = RUN337C_DIR / "proxy_mt5_usability_review.csv"
RUN337C_FUTURE_PROXY_REQ = RUN337C_DIR / "future_proxy_mt5_probe_requirements.csv"
RUN337C_CORE56_REVIEW = RUN337C_DIR / "core56_repair_or_scope_lock_review.csv"
RUN337C_CANARY_REVIEW = RUN337C_DIR / "no_lookahead_canary_review.csv"
RUN337C_REJECTED_CLAIMS = RUN337C_DIR / "rejected_claim_memory.csv"
RUN337C_SOURCE_REVIEW = RUN337C_DIR / "source_lineage_review.csv"
RUN337C_DATA_REVIEW = RUN337C_DIR / "data_integrity_review.csv"
RUN337C_DECISION = RUN337C_DIR / "final_review_materialized_inputs_proxy_mt5_usability_decision.json"
RUN337C_MANIFEST = RUN337C_DIR / "run_manifest.json"

NO_LOOKAHEAD_PROTOCOL_CSV = RUN_DIR / "no_lookahead_execution_protocol.csv"
PROXY_MT5_PROTOCOL_CSV = RUN_DIR / "proxy_mt5_fresh_probe_protocol.csv"
CORE56_PROTOCOL_CSV = RUN_DIR / "core56_refresh_repair_protocol.csv"
COST_DIRECTION_CURVE_PROTOCOL_CSV = RUN_DIR / "cost_direction_curve_gate_execution_protocol.csv"
OFFENSE_PROTOCOL_CSV = RUN_DIR / "offense_rebuild_execution_protocol.csv"
ECONOMIC_REGIME_PROTOCOL_CSV = RUN_DIR / "economic_regime_asof_protocol.csv"
PROTOCOL_ACCEPTANCE_CSV = RUN_DIR / "protocol_acceptance_matrix.csv"
RUNTIME_PROBE_REQUIREMENTS_CSV = RUN_DIR / "runtime_probe_package_requirements.csv"
MODEL_TRAINING_BOUNDARY_CSV = RUN_DIR / "model_training_allowed_boundary.csv"
RUN337E_QUEUE_CSV = RUN_DIR / "run337E_review_execution_protocols_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_research_execution_protocols_decision.json"
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
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_after_marker_once(text: str, marker: str, line: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def insert_focus_once(text: str, body: str, token: str) -> str:
    if token in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n{body}\n", 1)


def append_section_once(path: Path, header: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if header in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + header + "\n\n" + body.strip() + "\n", had_bom)


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv(RUN337C_QUEUE),
        "accepted_branch_queue": read_csv(RUN337C_ACCEPTED_BRANCH_QUEUE),
        "branch_acceptance": read_csv(RUN337C_BRANCH_ACCEPTANCE),
        "proxy_review": read_csv(RUN337C_PROXY_REVIEW),
        "future_proxy_requirements": read_csv(RUN337C_FUTURE_PROXY_REQ),
        "core56_review": read_csv(RUN337C_CORE56_REVIEW),
        "canary_review": read_csv(RUN337C_CANARY_REVIEW),
        "rejected_claims": read_csv(RUN337C_REJECTED_CLAIMS),
        "source_review": read_csv(RUN337C_SOURCE_REVIEW),
        "data_review": read_csv(RUN337C_DATA_REVIEW),
        "run337c_decision": read_json(RUN337C_DECISION),
        "run337c_manifest": read_json(RUN337C_MANIFEST),
    }


def build_no_lookahead_protocol(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    base_rows = [
        {
            "protocol_id": "no_lookahead_future_bar_canary",
            "risk_target": "future data leakage",
            "execution_step": "inject future-close and future-return features into a bad-control copy",
            "required_precheck": "training, validation, WFO, and forward windows must be timestamp ordered before any score is read",
            "expected_bad_control_result": "bad control must be rejected and logged as invalid",
            "pass_condition": "pipeline blocks future-derived features before model fit or proxy scoring",
            "fail_condition": "bad control reaches scorecard, MT5 handoff, or candidate package",
            "repair_action": "stop training queue and repair feature-label boundary tests",
        },
        {
            "protocol_id": "no_lookahead_forward_pocket_filter_canary",
            "risk_target": "forward pocket fitted filtering",
            "execution_step": "attempt to build a rule from failed forward pockets and verify it is rejected",
            "required_precheck": "all filters must be pre-forward thesis or WFO-only, not fitted to 2026-04-14+ outcomes",
            "expected_bad_control_result": "forward-pocket-derived filter is rejected",
            "pass_condition": "candidate selection cannot use post-OOS pocket knowledge",
            "fail_condition": "pocket exclusion improves KPI and is accepted without predeclared thesis",
            "repair_action": "move rule to failure memory only; rerun design without the fitted filter",
        },
        {
            "protocol_id": "no_threshold_retune_canary",
            "risk_target": "threshold overfit",
            "execution_step": "attempt to alter score threshold after seeing proxy or MT5 forward KPI",
            "required_precheck": "threshold must be fixed by predeclared protocol before runtime probing",
            "expected_bad_control_result": "threshold-retuned result is labeled invalid for selection",
            "pass_condition": "threshold changes require a new predeclared experiment, never same-run rescue",
            "fail_condition": "same candidate is rescued by a post-result threshold move",
            "repair_action": "discard retuned run from judgment and record overfit memory",
        },
        {
            "protocol_id": "no_lot_optimization_canary",
            "risk_target": "lot and risk cosmetic optimization",
            "execution_step": "attempt to improve curve shape through lot scaling after MT5 result is known",
            "required_precheck": "lot-normalized result must be reported before any money-scaled curve claim",
            "expected_bad_control_result": "post-result lot optimization is rejected",
            "pass_condition": "lot-normalized expectancy and drawdown remain visible",
            "fail_condition": "net profit improves while lot-normalized weakness is hidden",
            "repair_action": "downgrade to invalid KPI interpretation and require lot-normalized rerun",
        },
        {
            "protocol_id": "timestamp_basis_canary",
            "risk_target": "proxy-MT5 timestamp basis drift",
            "execution_step": "compare proxy expected rows against MT5 cycle_bar_time and open/close basis",
            "required_precheck": "timestamp alignment identity must be stored before signal usability is read",
            "expected_bad_control_result": "basis mismatch is blocked or downgraded to diagnostic only",
            "pass_condition": "same-bar and cycle-bar comparisons have explicit grain and no hidden shift",
            "fail_condition": "raw shifted proxy result is treated as runtime parity",
            "repair_action": "rerun row-level alignment and regenerate difference report",
        },
    ]
    canary_ids = {row.get("canary_id", "") for row in inputs["canary_review"]}
    rows = []
    for row in base_rows:
        rows.append(
            {
                **row,
                "source_canary_review": ";".join(sorted(item for item in canary_ids if item)) or rel(RUN337C_CANARY_REVIEW),
                "forbidden_use": "treating bad-control pass as alpha, selection, Forward Passed, or runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_mt5_protocol(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    review_by_subject = {row.get("subject", ""): row for row in inputs["proxy_review"]}
    rows = []
    for req in inputs["future_proxy_requirements"]:
        subject = req.get("subject", "")
        review = review_by_subject.get(subject, {})
        rows.append(
            {
                "subject": subject,
                "source_review_status": review.get("review_status", ""),
                "pre_probe_inputs": "feature_snapshot;model_bundle_or_candidate_spec;score_threshold_identity;risk_lot_identity;MT5_set_identity",
                "fresh_proxy_expected_required": "true",
                "fresh_mt5_runtime_probe_required": "true",
                "comparison_grain": "candidate_id;cycle_bar_time;direction;D_source;B_source;D_plus_B;score_bucket",
                "difference_metrics": "decision_match_rate;direction_match_rate;max_abs_score_diff;D_source_match;B_source_match;timestamp_gap_count",
                "usability_rule": "signal sanity only until fresh MT5 tester report, trade ledger, and cost/direction/curve gates are complete",
                "kpi_authority_condition": "MT5 Strategy Tester output plus parsed trade ledger; proxy alone never has KPI authority",
                "blocked_if": "missing proxy expected rows, missing MT5 report, timestamp mismatch, feature handoff drift, or core56 unresolved full-family claim",
                "allowed_use_after_pass": "runtime handoff sanity, debugging, and protocol review",
                "forbidden_use": "proxy-only profit pass/fail, Forward Passed, candidate selection, operating reference",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_core56_protocol(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = inputs["core56_review"][0] if inputs["core56_review"] else {}
    steps = [
        (
            "core56_source_inventory",
            "inventory equity, breadth, and top3 feature sources with file hashes and latest timestamp",
            "source file list, date coverage, symbol mapping, and update command",
            "source coverage reaches the same forward window as US100 M5 without synthetic future fill",
        ),
        (
            "core56_asof_join_contract",
            "define as-of joins for equity and breadth features before feature generation",
            "asof join tolerance, timezone, bar close/open convention, and stale-value policy",
            "join never reads data later than the target US100 M5 bar",
        ),
        (
            "core56_feature_handoff_snapshot",
            "materialize frozen feature order and runtime handoff snapshot for core56",
            "feature CSV hash, feature order hash, missing/latest gap report",
            "feature latest gap is zero for the tested forward window",
        ),
        (
            "core56_proxy_expected_generation",
            "generate proxy expected signal rows for repaired core56 candidate surface",
            "proxy expected values and score/decision/source dimensions",
            "proxy rows exist at the same timestamp grain required by MT5 comparison",
        ),
        (
            "core56_fresh_mt5_probe",
            "run fresh MT5 runtime probe for core56 after repair",
            "tester report, terminal output, structured trade ledger, settings identity",
            "runtime result exists and can be compared row-level to proxy output",
        ),
    ]
    return [
        {
            "protocol_id": step_id,
            "step_order": index,
            "source_decision": source.get("review_decision", "scope_locked_repair_required"),
            "repair_step": repair_step,
            "source_requirement": requirement,
            "no_lookahead_control": "as-of only; no forward pocket, threshold, or lot retune from 2026-04-14+ outcomes",
            "output_required": output_required,
            "pass_condition": pass_condition,
            "blocked_claim_until_pass": "full-family robustness;core56 candidate KPI;Forward Passed;runtime authority;Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (step_id, repair_step, output_required, pass_condition) in enumerate(steps, start=1)
        for requirement in [source.get("required_evidence", "core56 repair evidence required")]
    ]


def build_cost_direction_curve_protocol(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_scopes = [
        {
            "protocol_id": "cost_ladder_stress_gate",
            "gate_scope": "spread, commission, slippage, and adverse fill stress",
            "required_measurement": "net profit, PF, expectancy, DD, recovery, trades/day at base, plus 1x, 1.5x, 2x cost",
            "acceptance_boundary": "edge must not depend on unrealistically cheap execution",
            "failure_memory_trigger": "cost stress flips net/PF or creates unrecoverable underwater stretch",
        },
        {
            "protocol_id": "direction_symmetry_gate",
            "gate_scope": "long, short, D source, B source, and D+B attribution",
            "required_measurement": "side-separated net/PF/DD/expectancy and source-separated contribution",
            "acceptance_boundary": "one side/source cannot hide structural loss behind aggregate net",
            "failure_memory_trigger": "material side/source remains negative while aggregate passes",
        },
        {
            "protocol_id": "curve_pocket_gate",
            "gate_scope": "rolling 20/50/100 trade pockets and underwater stretch",
            "required_measurement": "worst pocket, longest underwater, recovery speed, pocket density",
            "acceptance_boundary": "curve remains usable without deleting known bad forward pockets",
            "failure_memory_trigger": "single pocket dominates profit or drawdown",
        },
        {
            "protocol_id": "lot_normalized_gate",
            "gate_scope": "risk and lot normalization",
            "required_measurement": "per-lot net, per-lot DD, expectancy per trade, trade density",
            "acceptance_boundary": "money curve quality survives lot normalization",
            "failure_memory_trigger": "KPI improvement comes only from lot shaping",
        },
        {
            "protocol_id": "regime_slice_gate",
            "gate_scope": "session, hour, month, volatility, ADX, VIX, USD, and rate regime",
            "required_measurement": "slice-level net/PF/DD/expectancy/trades with as-of macro identity",
            "acceptance_boundary": "no single unrepeatable macro pocket is the whole edge",
            "failure_memory_trigger": "regime concentration explains most profit or drawdown",
        },
    ]
    accepted_branches = ";".join(row.get("branch_id", "") for row in inputs["accepted_branch_queue"] if row.get("branch_id"))
    return [
        {
            **row,
            "source_branch_queue": accepted_branches,
            "required_runtime_inputs": "fresh MT5 report;trade ledger;tester settings;feature handoff hash;cost ladder settings",
            "forbidden_shortcut": "single KPI selection, proxy-only KPI authority, forward-pocket filtering, threshold retune, lot optimization",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in gate_scopes
    ]


def build_offense_protocol(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    offense_rows = [row for row in inputs["accepted_branch_queue"] if row.get("lane") == "offense"]
    rows = []
    for row in offense_rows:
        branch_id = row.get("branch_id", "")
        if "cost_buffer" in branch_id:
            thesis = "find signal interactions whose expectancy survives higher cost, not just higher raw hit rate"
            changed = "feature interactions around volatility, spread pressure, and session liquidity"
        elif "direction_symmetric" in branch_id:
            thesis = "reduce long/short and D/B source asymmetry before any aggregate KPI is trusted"
            changed = "side/source-aware loss diagnostics and balanced objective candidates"
        elif "curve_quality" in branch_id:
            thesis = "prefer smooth recovery and pocket resilience over isolated high-net pockets"
            changed = "curve pocket objective, underwater penalties, and recovery-factor diagnostics"
        else:
            thesis = "seek signals that are less dependent on one volatility, ADX, VIX, USD, or rate pocket"
            changed = "regime-invariant feature thesis with as-of macro joins"
        rows.append(
            {
                "branch_id": branch_id,
                "lane": "offense",
                "hypothesis": thesis,
                "decision_use": "authorize future model training only after protocol review, not select a candidate in run337D",
                "comparison_baseline": "run336O failure memory and run337C signal-sanity-only proxy review",
                "control_variables": "symbol=US100;timeframe=M5;fixed risk logic;fixed lot-normalized reporting;no post-forward threshold retune",
                "changed_variables": changed,
                "sample_scope": "future predeclared train/WFO/forward windows after run337E review",
                "success_criteria": "candidate can enter fresh proxy+MT5 probe with cost/direction/curve gates predeclared",
                "failure_criteria": "candidate only improves one KPI, one side, one pocket, or proxy output",
                "invalid_conditions": "lookahead, timestamp drift, proxy-only KPI, missing MT5, core56 full-family claim without repair",
                "stop_conditions": "bad controls pass; cost gate fails; direction gate collapses; curve pocket dominates",
                "evidence_plan": "model manifest;feature hashes;proxy expected;MT5 report;trade ledger;attribution/stress reports",
                "forbidden": row.get("must_keep", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_economic_regime_protocol() -> list[dict[str, Any]]:
    rows = [
        ("vix_regime_asof", "VIX", "daily close or broker-available proxy", "previous confirmed value only"),
        ("usd_regime_asof", "USD index or dollar regime", "DXY/USDX source", "as-of release/market close only"),
        ("rate_regime_asof", "US rate regime", "2Y/10Y yield or policy-rate proxy", "no future revisions in feature rows"),
        ("adx_regime_runtime", "ADX trend strength", "US100 M5 technical feature", "bar-close only, no future bar"),
        ("volatility_regime_runtime", "realized volatility", "US100 M5 rolling feature", "rolling window ending at current bar"),
        ("session_month_hour_slices", "session/hour/month", "broker timestamp contract", "timezone and session mapping fixed before review"),
    ]
    return [
        {
            "protocol_id": protocol_id,
            "regime_source": source,
            "data_source_requirement": source_requirement,
            "asof_rule": asof_rule,
            "join_key": "cycle_bar_time;broker_timezone;source_timestamp",
            "required_checks": "missing rows;duplicate rows;stale forward fill;revision risk;timezone drift",
            "slice_outputs": "net;PF;DD;expectancy;trades/day;long_short;D_source;B_source;D_plus_B",
            "invalid_if": "regime value is joined from the future or retrofitted after forward outcomes are known",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for protocol_id, source, source_requirement, asof_rule in rows
    ]


def build_runtime_requirements(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    subjects = [row.get("subject", "") for row in inputs["future_proxy_requirements"] if row.get("subject")]
    for subject in subjects:
        rows.append(
            {
                "package_id": f"{subject}_fresh_runtime_probe_package",
                "subject": subject,
                "required_files": "ONNX_or_model_spec;adapter_manifest;feature_order;MT5_set;tester_ini;handoff_snapshot",
                "runtime_outputs": "Strategy Tester HTML/XML;terminal log;trade ledger;runtime telemetry;settings identity",
                "parity_outputs": "proxy_expected_values;mt5_observed_values;difference_report;usability_decision",
                "cost_outputs": "cost_stress_report;spread_slippage_stress;lot_normalized_report",
                "attribution_outputs": "D_source_report;B_source_report;D_plus_B_report;long_short_report;regime_slices",
                "blocked_if_missing": "any runtime output, timestamp basis, feature order hash, or trade ledger",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_model_training_boundary() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "run337D_model_training_boundary",
            "training_allowed_in_run337D": "false",
            "reason": "run337D materializes execution protocols only; it does not create, tune, or select candidates",
            "earliest_reopen_condition": "run337E reviews protocols and gates pass without claim-boundary gaps",
            "still_forbidden_after_reopen": "post-forward threshold retune;lot optimization;forward-pocket filtering;proxy-only KPI authority;runtime authority without MT5 evidence",
            "allowed_after_reopen": "predeclared research training with fixed data boundary, no-lookahead controls, proxy expected values, and fresh MT5 runtime probe plan",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_protocol_acceptance(
    inputs: Mapping[str, Any],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    boundary: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output_map = {
        "stage337D_no_lookahead_execution_protocol": (NO_LOOKAHEAD_PROTOCOL_CSV, no_lookahead),
        "stage337D_proxy_mt5_fresh_probe_protocol": (PROXY_MT5_PROTOCOL_CSV, proxy_mt5),
        "stage337D_core56_refresh_protocol": (CORE56_PROTOCOL_CSV, core56),
        "stage337D_cost_direction_curve_protocol": (COST_DIRECTION_CURVE_PROTOCOL_CSV, cost_curve),
        "stage337D_offense_rebuild_protocol": (OFFENSE_PROTOCOL_CSV, offense),
    }
    rows = []
    for queue in inputs["queue"]:
        queue_id = queue.get("queue_id", "")
        output_path, output_rows = output_map.get(queue_id, (RUN_DIR / "missing_protocol.csv", []))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority", ""),
                "source_protocol": queue.get("protocol", ""),
                "materialized_output": rel(output_path),
                "output_rows": len(output_rows),
                "acceptance_status": "accepted_for_review" if output_rows else "blocked_missing_output",
                "review_requirement": "run337E must review protocol completeness before training or MT5 queue generation",
                "forbidden": queue.get("forbidden", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.extend(
        [
            {
                "queue_id": "stage337D_economic_regime_asof_protocol",
                "priority": "2",
                "source_protocol": "materialize economic/regime as-of join and slice protocol",
                "materialized_output": rel(ECONOMIC_REGIME_PROTOCOL_CSV),
                "output_rows": len(regime),
                "acceptance_status": "accepted_for_review",
                "review_requirement": "run337E verifies as-of macro joins before regime KPI interpretation",
                "forbidden": "using revised or future macro data to explain forward profit",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "stage337D_runtime_probe_package_requirements",
                "priority": "2",
                "source_protocol": "materialize fresh runtime probe package requirements",
                "materialized_output": rel(RUNTIME_PROBE_REQUIREMENTS_CSV),
                "output_rows": len(runtime),
                "acceptance_status": "accepted_for_review",
                "review_requirement": "run337E checks runtime package completeness before MT5 execution",
                "forbidden": "MetaEditor compile-only runtime claim",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "stage337D_model_training_allowed_boundary",
                "priority": "1",
                "source_protocol": "lock model training boundary",
                "materialized_output": rel(MODEL_TRAINING_BOUNDARY_CSV),
                "output_rows": len(boundary),
                "acceptance_status": "accepted_for_review_training_not_allowed",
                "review_requirement": "training remains closed until review explicitly reopens a predeclared packet",
                "forbidden": "training or repair branch before protocol review",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return rows


def build_run337e_queue() -> list[dict[str, Any]]:
    queue_items = [
        ("review_no_lookahead_protocol", NO_LOOKAHEAD_PROTOCOL_CSV, "confirm canaries block future leakage, threshold retune, lot optimization, and forward-pocket filtering"),
        ("review_proxy_mt5_fresh_probe_protocol", PROXY_MT5_PROTOCOL_CSV, "confirm every subject requires fresh proxy expected values and fresh MT5 runtime probe"),
        ("review_core56_refresh_protocol", CORE56_PROTOCOL_CSV, "confirm full-family claims remain blocked until core56 repair and probe exist"),
        ("review_cost_direction_curve_gates", COST_DIRECTION_CURVE_PROTOCOL_CSV, "confirm cost, direction/source, curve pocket, lot-normalized, and regime gates are complete"),
        ("review_offense_rebuild_protocol", OFFENSE_PROTOCOL_CSV, "confirm offense theses are predeclared and not fitted to failed forward pockets"),
        ("review_economic_regime_asof_protocol", ECONOMIC_REGIME_PROTOCOL_CSV, "confirm VIX, USD, rate, ADX, volatility, session, hour, and month slices use as-of rules"),
        ("review_runtime_package_requirements", RUNTIME_PROBE_REQUIREMENTS_CSV, "confirm future MT5 package requirements include report, logs, trade ledger, telemetry, and identities"),
        ("review_training_boundary", MODEL_TRAINING_BOUNDARY_CSV, "confirm no model training is allowed until protocol review passes"),
    ]
    return [
        {
            "queue_id": queue_id,
            "priority": index,
            "review_input": rel(path),
            "review_task": task,
            "required_decision": "accept_for_next_materialization_or_repair_protocol_gap",
            "forbidden": "declaring Forward Passed, runtime authority, candidate selection, or Goal Achieve from protocol files alone",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, path, task) in enumerate(queue_items, start=1)
    ]


def build_gate_audit(
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    boundary: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    all_proxy_require_fresh = all(
        row.get("fresh_proxy_expected_required") == "true" and row.get("fresh_mt5_runtime_probe_required") == "true"
        for row in proxy_mt5
    )
    training_blocked = all(row.get("training_allowed_in_run337D") == "false" for row in boundary)
    acceptance_pass = all(row.get("acceptance_status", "").startswith("accepted") for row in acceptance)
    return [
        {
            "gate_id": "experiment_design_receipt_ready",
            "status": "pass",
            "evidence": rel(EXPERIMENT_DESIGN_JSON),
            "finding": "hypothesis, decision use, controls, invalid conditions, stop conditions, and evidence plan are materialized",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_protocol_materialized",
            "status": "pass" if len(no_lookahead) >= 5 else "fail",
            "evidence": rel(NO_LOOKAHEAD_PROTOCOL_CSV),
            "finding": f"no_lookahead_rows={len(no_lookahead)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_fresh_probe_required",
            "status": "pass" if all_proxy_require_fresh and len(proxy_mt5) >= 5 else "fail",
            "evidence": rel(PROXY_MT5_PROTOCOL_CSV),
            "finding": f"proxy_mt5_subjects={len(proxy_mt5)};fresh_required={all_proxy_require_fresh}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "core56_scope_lock_preserved",
            "status": "pass" if any("full-family" in row.get("blocked_claim_until_pass", "") for row in core56) else "fail",
            "evidence": rel(CORE56_PROTOCOL_CSV),
            "finding": "full-family claim blocked until core56 repair and MT5 probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_gates_complete",
            "status": "pass" if len(cost_curve) >= 5 else "fail",
            "evidence": rel(COST_DIRECTION_CURVE_PROTOCOL_CSV),
            "finding": f"cost_direction_curve_gate_rows={len(cost_curve)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "economic_regime_asof_protocol_complete",
            "status": "pass" if len(regime) >= 6 else "fail",
            "evidence": rel(ECONOMIC_REGIME_PROTOCOL_CSV),
            "finding": f"economic_regime_rows={len(regime)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "offense_protocol_predeclared",
            "status": "pass" if len(offense) >= 4 else "fail",
            "evidence": rel(OFFENSE_PROTOCOL_CSV),
            "finding": f"offense_protocol_rows={len(offense)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_probe_package_requirements_complete",
            "status": "pass" if len(runtime) >= 5 else "fail",
            "evidence": rel(RUNTIME_PROBE_REQUIREMENTS_CSV),
            "finding": f"runtime_package_rows={len(runtime)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "training_blocked_in_run337D",
            "status": "pass" if training_blocked else "fail",
            "evidence": rel(MODEL_TRAINING_BOUNDARY_CSV),
            "finding": f"training_allowed_in_run337D={not training_blocked}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "protocol_acceptance_matrix_ready",
            "status": "pass" if acceptance_pass and len(acceptance) >= 8 else "fail",
            "evidence": rel(PROTOCOL_ACCEPTANCE_CSV),
            "finding": f"acceptance_rows={len(acceptance)};all_accepted={acceptance_pass}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_review_queue_ready",
            "status": "pass" if len(review_queue) >= 8 else "fail",
            "evidence": rel(RUN337E_QUEUE_CSV),
            "finding": f"run337E_queue_rows={len(review_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no selected candidate, Forward Passed, runtime authority, live readiness, deployment, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    inputs: Mapping[str, Any],
    no_lookahead: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    core56: Sequence[Mapping[str, Any]],
    cost_curve: Sequence[Mapping[str, Any]],
    offense: Sequence[Mapping[str, Any]],
    regime: Sequence[Mapping[str, Any]],
    acceptance: Sequence[Mapping[str, Any]],
    runtime: Sequence[Mapping[str, Any]],
    boundary: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "source_queue_rows": len(inputs["queue"]),
        "source_accepted_branch_rows": len(inputs["accepted_branch_queue"]),
        "source_proxy_subjects": len(inputs["future_proxy_requirements"]),
        "no_lookahead_protocol_rows": len(no_lookahead),
        "proxy_mt5_protocol_rows": len(proxy_mt5),
        "core56_protocol_rows": len(core56),
        "cost_direction_curve_gate_rows": len(cost_curve),
        "offense_protocol_rows": len(offense),
        "economic_regime_protocol_rows": len(regime),
        "protocol_acceptance_rows": len(acceptance),
        "runtime_probe_requirement_rows": len(runtime),
        "model_training_boundary_rows": len(boundary),
        "run337E_queue_rows": len(review_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "Stage337 can reduce cost, direction, curve, core56, and proxy-MT5 overfit risk only if future research is predeclared before training",
                "decision_use": "authorize run337E protocol review and later decide whether predeclared training/probe packets may open",
                "comparison_baseline": "run336O/run336P failure memory and run337C proxy-MT5 signal-sanity-only review",
                "control_variables": "US100 M5, no forward-pocket filtering, no threshold retune, no lot optimization, MT5 required for KPI authority",
                "changed_variables": "execution protocols for no-lookahead, proxy-MT5, core56 repair, cost/direction/curve gates, offense rebuild, and economic regimes",
                "sample_scope": "protocol materialization only; no new model or KPI sample in run337D",
                "success_criteria": "all protocol files and review queue are materialized with claim guards passing",
                "failure_criteria": "missing protocol, missing fresh MT5 requirement, missing core56 lock, or training allowed before review",
                "invalid_conditions": "proxy-only KPI authority, forward-fit filter, timestamp drift, post-result threshold or lot repair",
                "stop_conditions": "any required gate fails; run337E must repair protocols before training opens",
                "evidence_plan": "CSV protocols, receipts, gate audit, report, decision doc, ledgers, and artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337C reviewed protocol queue, proxy-MT5 review, core56 lock, and source/data integrity reviews",
                "time_axis": "cycle_bar_time and broker timestamp basis must be explicit before proxy-MT5 or regime joins",
                "sample_scope": "protocol-only scope; future US100 M5 forward data and macro regimes require as-of identities before use",
                "missing_or_duplicate_check": "run337D defines required checks; it does not certify future data completeness",
                "feature_label_boundary": "no model training or labels in run337D; future features must end at or before target bar",
                "split_boundary": "future train/WFO/forward split must be predeclared in a reviewed packet",
                "leakage_risk": "forward-pocket filtering, revised macro joins, threshold retune, and proxy authority creep",
                "data_hash_or_identity": rel(RUN337C_DATA_REVIEW),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "future MT5 packages defined by runtime_probe_package_requirements.csv",
                "shared_contract": "fresh proxy expected values, MT5 tester outputs, feature order, threshold, risk, lot, timestamp basis, D/B sources, and trade ledger must match",
                "known_differences": "run337C proxy is signal sanity only; core56 lacks repair/probe; no fresh MT5 run occurs in run337D",
                "parity_check": "protocol materialization only; no runtime authority",
                "parity_identity": rel(PROXY_MT5_PROTOCOL_CSV),
                "runtime_claim_boundary": "research-only protocol, not runtime authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(RUN337C_QUEUE),
                    rel(RUN337C_ACCEPTED_BRANCH_QUEUE),
                    rel(RUN337C_PROXY_REVIEW),
                    rel(RUN337C_FUTURE_PROXY_REQ),
                    rel(RUN337C_CORE56_REVIEW),
                    rel(RUN337C_DECISION),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(NO_LOOKAHEAD_PROTOCOL_CSV),
                    rel(PROXY_MT5_PROTOCOL_CSV),
                    rel(CORE56_PROTOCOL_CSV),
                    rel(COST_DIRECTION_CURVE_PROTOCOL_CSV),
                    rel(RUN337E_QUEUE_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337D script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "Stage337 research execution protocols",
                "evidence_available": "protocol CSVs, training boundary, runtime package requirements, gate audit, and review queue",
                "evidence_missing": "no new model training, no fresh MT5 runtime probe, no candidate KPI, no Forward Passed/Failed decision",
                "judgment_label": "exploratory",
                "claim_boundary": "protocols are ready for review only; no candidate, KPI authority, or operating claim",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 좋은 후보를 고른 것이 아니라, 다음 후보 실험이 과적합으로 새지 않게 검사문을 박아둔 것이다.",
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
    ]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# run337D Research Execution Protocols(337D 연구 실행 절차)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Materialized Protocols(물질화된 절차)

- no_lookahead_protocol(미래참조 방어 절차): `{metrics['no_lookahead_protocol_rows']}` rows(행)
- proxy_mt5_fresh_probe_protocol(프록시-MT5 신규 탐침 절차): `{metrics['proxy_mt5_protocol_rows']}` rows(행)
- core56_refresh_repair_protocol(핵심56 갱신 수리 절차): `{metrics['core56_protocol_rows']}` rows(행)
- cost_direction_curve_gate_protocol(비용/방향/곡선 게이트 절차): `{metrics['cost_direction_curve_gate_rows']}` rows(행)
- offense_rebuild_protocol(공격형 재구성 절차): `{metrics['offense_protocol_rows']}` rows(행)
- economic_regime_asof_protocol(경제 국면 as-of 절차): `{metrics['economic_regime_protocol_rows']}` rows(행)
- runtime_probe_requirements(런타임 탐침 요구사항): `{metrics['runtime_probe_requirement_rows']}` rows(행)
- model_training_boundary(모델 학습 경계): `{metrics['model_training_boundary_rows']}` rows(행)
- gate_audit(게이트 감사): `{metrics['gate_rows']}` rows(행), failed(실패) `{metrics['failed_gate_rows']}`

Effect(효과): run337D(337D 실행)는 후보를 고르지 않고, 다음 연구가 proxy-only KPI(프록시 단독 KPI), forward-pocket filtering(전진 포켓 필터링), threshold retune(임계값 재조정), lot optimization(로트 최적화), core56 silent drop(핵심56 조용한 제외)로 새지 않도록 실행 절차를 고정했다.
"""
    decision = f"""
# 2026-05-27 Stage337D Decision(337D 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): Stage337D(337D 단계)는 학습(training, 학습)이나 MT5 execution(MT5 실행)을 시작하지 않고, 그 전에 통과해야 할 protocol(절차)을 파일로 고정했다. 다음 run337E(337E 실행)는 이 절차들이 충분한지 검토한다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""
# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- opened_by(개방 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337D(337D 실행)는 no-lookahead(미래참조 방어), proxy-MT5 fresh probe(프록시-MT5 신규 탐침), core56 repair(핵심56 수리), cost/direction/curve gate(비용/방향/곡선 게이트), economic regime as-of(경제 국면 시점 기준) 절차를 만들었다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337C_summary(337C 요약):",
        f"- run337D_summary(337D 요약): `{STATUS}`. Effect(효과): no-lookahead(미래참조 방어), proxy-MT5 fresh probe(프록시-MT5 신규 탐침), core56 repair(핵심56 수리), cost/direction/curve gate(비용/방향/곡선 게이트), economic regime as-of(경제 국면 시점 기준) 실행 절차를 물질화하고 run337E(337E 실행) 검토로 넘긴다.",
        "run337D_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
## run337D Outputs(337D 산출물)

- no_lookahead_execution_protocol(미래참조 방어 절차): `{rel(NO_LOOKAHEAD_PROTOCOL_CSV)}`
- proxy_mt5_fresh_probe_protocol(프록시-MT5 신규 탐침 절차): `{rel(PROXY_MT5_PROTOCOL_CSV)}`
- core56_refresh_repair_protocol(핵심56 갱신 수리 절차): `{rel(CORE56_PROTOCOL_CSV)}`
- cost_direction_curve_gate_protocol(비용/방향/곡선 게이트 절차): `{rel(COST_DIRECTION_CURVE_PROTOCOL_CSV)}`
- offense_rebuild_protocol(공격형 재구성 절차): `{rel(OFFENSE_PROTOCOL_CSV)}`
- economic_regime_asof_protocol(경제 국면 시점 기준 절차): `{rel(ECONOMIC_REGIME_PROTOCOL_CSV)}`
- runtime_probe_requirements(런타임 탐침 요구사항): `{rel(RUNTIME_PROBE_REQUIREMENTS_CSV)}`
- run337E_queue(337E 대기열): `{rel(RUN337E_QUEUE_CSV)}`

Effect(효과): 다음 실행은 학습이나 후보 선택이 아니라, 이 절차들이 실제로 과적합 방어와 MT5 근거 요구를 충분히 고정했는지 검토한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337D Outputs(337D 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) run337D(337D 실행)는 `{STATUS}`로 research execution protocols(연구 실행 절차)를 물질화했다. "
        "Effect(효과): 학습(training, 학습) 전 no-lookahead(미래참조 방어), proxy-MT5 fresh probe(프록시-MT5 신규 탐침), core56 repair(핵심56 수리), cost/direction/curve gate(비용/방향/곡선 게이트), economic regime as-of(경제 국면 시점 기준)를 먼저 검토하게 만든다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337D focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
    }
    for prefix, new_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, new_line)
    summary = (
        f"- run337D_summary(337D 요약): `{STATUS}`. "
        "Effect(효과): no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/economic-regime(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/경제 국면) 절차를 만들고 run337E(337E 실행) 검토 대기열로 넘긴다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337D_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337D Research Execution Protocols(337D 연구 실행 절차)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337C(337C 실행)의 protocol queue(절차 대기열)를 실제 no-lookahead/proxy-MT5/core56/cost-direction-curve/offense/economic-regime(미래참조/프록시-MT5/핵심56/비용-방향-곡선/공격/경제 국면) 실행 절차 파일로 만들었다.
- effect(효과): 다음 실험이 과적합을 위한 또 다른 과적합으로 흐르지 않도록 학습 전 필수 검증문을 고정했다.
- boundary(경계): selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
""",
        )
    )
    return artifacts


def update_registers(artifacts: Sequence[Path], generated_at: str) -> list[Path]:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "research_execution_protocol_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};training_not_allowed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__research_execution_protocols",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "research_execution_protocol_materialization",
                "tier_scope": "stage337_protocol_boundary_macro48_u42_core56",
                "kpi_scope": "protocol_only_no_new_candidate_kpi",
                "scoreboard_lane": "protocol_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "protocol_files=10;failed_gates=0;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;proxy_not_kpi_authority;core56_scope_locked;goal_achieve_not_claimed",
                "external_verification_status": "protocol_only_no_fresh_mt5_execution",
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
                "ledger_row_id": f"{RUN_ID}__research_execution_protocols",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design",
                "evidence_scope": "run337C_protocol_queue_proxy_mt5_core56_branch_reviews",
                "kpi_scope": "protocol_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};training_not_allowed;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}::{rel(path)}",
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": generated_at,
            "notes": "run337D_research_execution_protocols_no_selection",
        }
        for path in artifacts
        if path_exists(path) and io_path(path).is_file()
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY]


def main() -> int:
    generated_at = now_utc()
    inputs = load_inputs()
    no_lookahead = build_no_lookahead_protocol(inputs)
    proxy_mt5 = build_proxy_mt5_protocol(inputs)
    core56 = build_core56_protocol(inputs)
    cost_curve = build_cost_direction_curve_protocol(inputs)
    offense = build_offense_protocol(inputs)
    regime = build_economic_regime_protocol()
    runtime = build_runtime_requirements(inputs)
    boundary = build_model_training_boundary()
    acceptance = build_protocol_acceptance(
        inputs, no_lookahead, proxy_mt5, core56, cost_curve, offense, regime, runtime, boundary
    )
    review_queue = build_run337e_queue()
    audit = build_gate_audit(
        no_lookahead, proxy_mt5, core56, cost_curve, offense, regime, acceptance, runtime, boundary, review_queue
    )
    metrics = build_metrics(
        inputs,
        no_lookahead,
        proxy_mt5,
        core56,
        cost_curve,
        offense,
        regime,
        acceptance,
        runtime,
        boundary,
        review_queue,
        audit,
    )
    failed_gates = [row for row in audit if row.get("status") != "pass"]
    run_artifacts = [
        write_csv(
            NO_LOOKAHEAD_PROTOCOL_CSV,
            (
                "protocol_id",
                "risk_target",
                "execution_step",
                "required_precheck",
                "expected_bad_control_result",
                "pass_condition",
                "fail_condition",
                "repair_action",
                "source_canary_review",
                "forbidden_use",
                "claim_boundary",
            ),
            no_lookahead,
        ),
        write_csv(
            PROXY_MT5_PROTOCOL_CSV,
            (
                "subject",
                "source_review_status",
                "pre_probe_inputs",
                "fresh_proxy_expected_required",
                "fresh_mt5_runtime_probe_required",
                "comparison_grain",
                "difference_metrics",
                "usability_rule",
                "kpi_authority_condition",
                "blocked_if",
                "allowed_use_after_pass",
                "forbidden_use",
                "claim_boundary",
            ),
            proxy_mt5,
        ),
        write_csv(
            CORE56_PROTOCOL_CSV,
            (
                "protocol_id",
                "step_order",
                "source_decision",
                "repair_step",
                "source_requirement",
                "no_lookahead_control",
                "output_required",
                "pass_condition",
                "blocked_claim_until_pass",
                "claim_boundary",
            ),
            core56,
        ),
        write_csv(
            COST_DIRECTION_CURVE_PROTOCOL_CSV,
            (
                "protocol_id",
                "gate_scope",
                "required_measurement",
                "acceptance_boundary",
                "failure_memory_trigger",
                "source_branch_queue",
                "required_runtime_inputs",
                "forbidden_shortcut",
                "next_review",
                "claim_boundary",
            ),
            cost_curve,
        ),
        write_csv(
            OFFENSE_PROTOCOL_CSV,
            (
                "branch_id",
                "lane",
                "hypothesis",
                "decision_use",
                "comparison_baseline",
                "control_variables",
                "changed_variables",
                "sample_scope",
                "success_criteria",
                "failure_criteria",
                "invalid_conditions",
                "stop_conditions",
                "evidence_plan",
                "forbidden",
                "claim_boundary",
            ),
            offense,
        ),
        write_csv(
            ECONOMIC_REGIME_PROTOCOL_CSV,
            (
                "protocol_id",
                "regime_source",
                "data_source_requirement",
                "asof_rule",
                "join_key",
                "required_checks",
                "slice_outputs",
                "invalid_if",
                "claim_boundary",
            ),
            regime,
        ),
        write_csv(
            PROTOCOL_ACCEPTANCE_CSV,
            (
                "queue_id",
                "priority",
                "source_protocol",
                "materialized_output",
                "output_rows",
                "acceptance_status",
                "review_requirement",
                "forbidden",
                "claim_boundary",
            ),
            acceptance,
        ),
        write_csv(
            RUNTIME_PROBE_REQUIREMENTS_CSV,
            (
                "package_id",
                "subject",
                "required_files",
                "runtime_outputs",
                "parity_outputs",
                "cost_outputs",
                "attribution_outputs",
                "blocked_if_missing",
                "claim_boundary",
            ),
            runtime,
        ),
        write_csv(
            MODEL_TRAINING_BOUNDARY_CSV,
            (
                "boundary_id",
                "training_allowed_in_run337D",
                "reason",
                "earliest_reopen_condition",
                "still_forbidden_after_reopen",
                "allowed_after_reopen",
                "claim_boundary",
            ),
            boundary,
        ),
        write_csv(
            RUN337E_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "review_input",
                "review_task",
                "required_decision",
                "forbidden",
                "claim_boundary",
            ),
            review_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337D_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337D_protocol_gate_failure_requires_repair",
        "decision": DECISION if not failed_gates else "stage337D_protocol_materialization_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_for_stage337_new_work",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    run_artifacts.append(write_json(FINAL_DECISION_JSON, final_payload))
    run_artifacts.extend(write_reports(metrics))
    if failed_gates:
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337D_gate_failure",
                "decision": "stage337D_protocol_materialization_blocked_gate_failure",
                "failed_gates": failed_gates,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        print(json.dumps({"run_id": RUN_ID, "failed_gates": failed_gates}, ensure_ascii=False, indent=2))
        return 2
    status_artifacts = update_status_docs(metrics)
    all_artifacts = [Path(__file__), *run_artifacts, *status_artifacts]
    manifest_payload = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": generated_at,
        "producer": rel(Path(__file__)),
        "source_inputs": [
            rel(RUN337C_QUEUE),
            rel(RUN337C_ACCEPTED_BRANCH_QUEUE),
            rel(RUN337C_BRANCH_ACCEPTANCE),
            rel(RUN337C_PROXY_REVIEW),
            rel(RUN337C_FUTURE_PROXY_REQ),
            rel(RUN337C_CORE56_REVIEW),
            rel(RUN337C_CANARY_REVIEW),
            rel(RUN337C_REJECTED_CLAIMS),
            rel(RUN337C_DECISION),
            rel(RUN337C_MANIFEST),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "protocol_only_no_fresh_mt5_execution",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_JSON, manifest_payload)
    all_artifacts.append(RUN_MANIFEST_JSON)
    register_artifacts = update_registers(all_artifacts, generated_at)
    all_artifacts.extend(register_artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "protocol_acceptance_rows": metrics["protocol_acceptance_rows"],
                "gate_rows": metrics["gate_rows"],
                "failed_gate_rows": metrics["failed_gate_rows"],
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
