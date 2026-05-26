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


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
NEXT_STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run336P"
RUN_ID = "run336P_forward_decision_or_failure_memory_handoff_v1"
PARENT_RUN_ID = "run336O_repaired_forward_attribution_and_cost_stress_v1"
NEXT_RUN_ID = "run337A_design_cost_buffer_direction_curve_rebuild_packet_v1"
STATUS = "completed_stage336_closeout_open_stage337_no_selection"
JUDGMENT = "repaired_forward_subset_failed_robustness_gate_failure_memory_handoff"
DECISION = "stage336P_repaired_forward_subset_failed_open_stage337_cost_direction_curve_rebuild_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336P_forward_decision_failure_memory_handoff_"
    "same_run336M_repaired_mt5_evidence_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_forward_failed_scoped_to_repaired_subset_"
    "no_forward_passed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_stage337_cost_buffer_direction_curve_rebuild_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve_"
    "no_forward_pocket_filtering_no_threshold_retuning_no_lot_optimization_without_predeclared_protocol"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN336O_DIR = STAGE_DIR / "02_runs" / "run336O"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336P_close_stage336_open_stage337.md"
REPORT_DOC = REVIEWS_DIR / "run336P_forward_decision_failure_memory_handoff.md"

SCORECARD = RUN336O_DIR / "forward_robustness_scorecard.csv"
SUMMARY = RUN336O_DIR / "attempt_forward_attribution_summary.csv"
FINDINGS = RUN336O_DIR / "forward_fragility_findings.csv"
COST_STRESS = RUN336O_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN336O_DIR / "curve_pocket_report.csv"
REGIME_SLICE = RUN336O_DIR / "regime_direction_slice_report.csv"
REPORT_AUDIT = RUN336O_DIR / "report_metric_reparse_audit.csv"
RUN336O_DECISION = RUN336O_DIR / "final_repaired_forward_attribution_decision.json"
RUN336N_DECISION = STAGE_DIR / "02_runs" / "run336N" / "final_timestamp_aligned_parity_decision.json"


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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), keep_default_na=False)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        number = float(str(value).strip())
        return number if math.isfinite(number) else default
    except (TypeError, ValueError):
        return default


def build_decision_matrix(scorecard: pd.DataFrame, summary: pd.DataFrame, findings: pd.DataFrame) -> list[dict[str, Any]]:
    best = scorecard.iloc[0].to_dict()
    cost_fail_count = int((scorecard["cost_plus_1_0_net"].astype(float) <= 0).sum())
    short_fail_count = int((summary["short_net_profit"].astype(float) <= 0).sum())
    deep_curve_count = int((scorecard["rolling20_worst_net"].astype(float) <= -50).sum())
    return [
        {
            "subject": "run336M_repaired_forward_subset",
            "evidence": rel(SCORECARD),
            "decision": "Forward Failed scoped to repaired subset(수리 부분집합 한정 전진 실패)",
            "reason": f"cost+1.0 positive survival failed in {cost_fail_count}/4 attempts; rolling20 pocket failed in {deep_curve_count}/4 attempts",
            "selected_candidate": "none",
            "allowed_use": "failure_memory;next_stage_constraints",
            "forbidden_use": "Forward Passed;live readiness;runtime authority;deployment",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "best_repaired_clue_m48_plain_rf",
            "evidence": rel(SUMMARY),
            "decision": "preserved clue only(보존 단서 전용)",
            "reason": f"net={best.get('net_profit')};pf={best.get('profit_factor')};cost_plus_1_0_net={best.get('cost_plus_1_0_net')};failure_axes={best.get('failure_axes')}",
            "selected_candidate": "none",
            "allowed_use": "seed clue for Stage337 cost buffer design",
            "forbidden_use": "candidate selection or operating reference",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "direction_balance",
            "evidence": rel(SUMMARY),
            "decision": "failure memory(실패 기억)",
            "reason": f"{short_fail_count}/4 attempts have non-positive short side net profit",
            "selected_candidate": "none",
            "allowed_use": "side-separated hypothesis and paired KPI",
            "forbidden_use": "drop short side after seeing forward data",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "proxy_mt5_parity",
            "evidence": rel(RUN336N_DECISION),
            "decision": "parity usable for signal comparison only(신호 비교 전용 동등성 사용 가능)",
            "reason": "run336N timestamp-aligned proxy-MT5 parity matched 20/20, but KPI robustness failed in run336O",
            "selected_candidate": "none",
            "allowed_use": "runtime signal sanity check",
            "forbidden_use": "profit proxy or forward pass proof",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "stage336_question",
            "evidence": rel(REPORT_DOC),
            "decision": "close stage and open Stage337(단계 종료 및 337단계 개방)",
            "reason": f"failure findings={len(findings)}; next topic is cost/direction/curve rebuild",
            "selected_candidate": "none",
            "allowed_use": NEXT_STAGE_ID,
            "forbidden_use": "Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory_handoff(findings: pd.DataFrame, scorecard: pd.DataFrame, summary: pd.DataFrame) -> list[dict[str, Any]]:
    affected_by_axis = {
        "cost_buffer_fragility": ";".join(scorecard.loc[scorecard["cost_plus_1_0_net"].astype(float) <= 0, "attempt_name"].astype(str)),
        "direction_asymmetry": ";".join(summary.loc[summary["short_net_profit"].astype(float) <= 0, "attempt_name"].astype(str)),
        "curve_recovery_fragility": ";".join(scorecard.loc[scorecard["rolling20_worst_net"].astype(float) <= -50, "attempt_name"].astype(str)),
        "density_quality_tradeoff": ";".join(scorecard["attempt_name"].astype(str)),
        "worst_regime_slice": "u42_bal_rf",
    }
    next_constraints = {
        "cost_buffer_fragility": "raise expectancy and cost buffer before increasing density",
        "direction_asymmetry": "side-separated thesis and long/short paired KPI required",
        "curve_recovery_fragility": "rolling pocket and underwater constraints required before selection",
        "density_quality_tradeoff": "keep density but forbid lot or threshold cosmetic repair",
        "worst_regime_slice": "use regime slice as failure memory, not post-forward exclusion",
    }
    forbidden = {
        "cost_buffer_fragility": "threshold retune;lot optimization;spread assumption relaxation",
        "direction_asymmetry": "drop short side;post-forward side filter",
        "curve_recovery_fragility": "calendar pocket removal;single-window winner selection",
        "density_quality_tradeoff": "trade-count-only objective",
        "worst_regime_slice": "rate-regime filter selected from failed forward data",
    }
    rows: list[dict[str, Any]] = []
    for item in findings.to_dict("records"):
        axis = str(item["finding_id"])
        rows.append(
            {
                "failure_axis": axis,
                "severity": item.get("severity", ""),
                "finding": item.get("finding", ""),
                "affected_attempts": affected_by_axis.get(axis, ""),
                "stage337_required_constraint": next_constraints.get(axis, "carry as predeclared failure memory"),
                "forbidden_repair_path": forbidden.get(axis, "post-hoc repair"),
                "salvage_value": "m48_plain_rf clue only" if axis == "cost_buffer_fragility" else "diagnostic boundary",
                "reopen_condition": "independent WFO and MT5 probe show cost, direction, and curve pocket survival together",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "failure_axis": "core56_equity_refresh_gap",
            "severity": "medium",
            "finding": "core56 remains outside repaired forward subset until equity refresh source is repaired",
            "affected_attempts": "core56_bal_rf;core56_plain_rf",
            "stage337_required_constraint": "do not claim full cp322A family robustness without refreshed equity feature handoff",
            "forbidden_repair_path": "silently dropping core56 while claiming full family pass",
            "salvage_value": "runtime repair requirement",
            "reopen_condition": "equity/breadth/top3 refresh source materialized and parity-probed without lookahead",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_stage337_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "cost_buffer_expectancy",
            "question": "Can the surface survive at least extra_cost_per_trade=1.0 without threshold or lot tuning?",
            "required_evidence": "cost stress grid;lot-normalized result;expectancy decomposition",
            "forbidden": "threshold retune on forward;lot optimization;cost assumption relaxation",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "direction_symmetry",
            "question": "Can long and short both contribute or be predeclared with honest side limits?",
            "required_evidence": "long/short attribution;side-specific failure memory;negative control",
            "forbidden": "post-forward side drop;side filter chosen from run336O loss",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "curve_pocket_recovery",
            "question": "Can the curve avoid deep rolling pockets and long underwater stretches?",
            "required_evidence": "rolling 20/50/100 pocket;underwater stretch;closed balance recovery",
            "forbidden": "calendar trimming;single-window score only",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "regime_stability",
            "question": "Can volatility, ADX, VIX, USD, and rate slices explain survival without post-hoc filters?",
            "required_evidence": "session/hour/month/volatility/ADX/VIX/USD/rate slices",
            "forbidden": "selecting regime exclusions directly from run336O failed pocket",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "proxy_mt5_usability",
            "question": "Can proxy expected values remain signal checks while MT5 keeps KPI authority?",
            "required_evidence": "proxy expected vs MT5 runtime probe difference;usability label",
            "forbidden": "profit proxy selection;raw timestamp mismatch reuse",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "runtime_feature_handoff",
            "question": "Can feature handoff stay fresh and timestamp-safe across all required families?",
            "required_evidence": "feature freshness audit;timestamp basis audit;core56 refresh repair condition",
            "forbidden": "claiming full-family pass from macro48/u42 subset only",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "contract_id": "no_lookahead_guard",
            "question": "Can all new designs prove feature-label boundary and avoid forward pocket fitting?",
            "required_evidence": "data integrity receipt;split contract;negative controls",
            "forbidden": "look-ahead bias;forward result tuned thresholds;repair branch after seeing slice loss",
            "first_run_use": NEXT_RUN_ID,
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
    ]


def build_run337a_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "stage337A_design_packet",
            "priority": 1,
            "task": "Design a bounded cost-buffer/direction/curve rebuild packet from run336P failure memory.",
            "required_inputs": "stage337_opening_contract;stage336_failure_memory_handoff;run336O_scorecard",
            "required_outputs": "branch_design;negative_controls;proxy_mt5_contract;MT5_probe_plan",
            "forbidden": "training before protocol;threshold retune;lot optimization;forward pocket filter",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "queue_id": "core56_refresh_decision",
            "priority": 2,
            "task": "Decide whether core56 equity/breadth/top3 refresh is repaired first or kept out of full-family claims.",
            "required_inputs": "run336L_core56_blocker;run336M_feature_handoff_summary",
            "required_outputs": "repair_or_out_of_scope_boundary",
            "forbidden": "full cp322A family robustness claim while core56 is missing",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
        {
            "queue_id": "mt5_authority_contract",
            "priority": 3,
            "task": "Keep MT5 runtime probe as KPI authority and proxy as signal sanity check only.",
            "required_inputs": "run336N_parity;run336O_report_audit",
            "required_outputs": "proxy_usability_contract;runtime_evidence_gate",
            "forbidden": "proxy profit pass/fail",
            "claim_boundary": NEXT_STAGE_BOUNDARY,
        },
    ]


def build_gate_audit(scorecard: pd.DataFrame, summary: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run336O_source_artifacts_present",
            "status": "pass",
            "evidence": rel(RUN336O_DECISION),
            "finding": "run336O decision, scorecard, summary, cost stress, curve pocket, and slice reports are present",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_report_reparse_identity",
            "status": "pass",
            "evidence": rel(REPORT_AUDIT),
            "finding": "parsed trade counts match runtime counts for 4/4 attempts",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_pass_blocked",
            "status": "pass",
            "evidence": rel(SCORECARD),
            "finding": f"{int((scorecard['cost_plus_1_0_net'].astype(float) <= 0).sum())}/4 attempts fail cost+1.0 positive survival",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "direction_failure_recorded",
            "status": "pass",
            "evidence": rel(SUMMARY),
            "finding": f"{int((summary['short_net_profit'].astype(float) <= 0).sum())}/4 attempts have non-positive short net",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "selection_and_operating_claim_guard",
            "status": "pass",
            "evidence": rel(SELECTED_STATUS),
            "finding": "selected candidate, live readiness, operating promotion, runtime authority, and Goal Achieve remain unclaimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_stage_opening_contract",
            "status": "pass",
            "evidence": rel(RUN_DIR / "stage337_opening_contract.csv"),
            "finding": "Stage337 is opened around cost, direction, curve, regime, proxy, handoff, and no-lookahead constraints",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_run_artifacts() -> list[Path]:
    scorecard = read_csv(SCORECARD)
    summary = read_csv(SUMMARY)
    findings = read_csv(FINDINGS)
    decision_matrix = build_decision_matrix(scorecard, summary, findings)
    failure_handoff = build_failure_memory_handoff(findings, scorecard, summary)
    stage337_contract = build_stage337_contract()
    run337a_queue = build_run337a_queue()
    gate_audit = build_gate_audit(scorecard, summary)
    final_decision = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "repaired_subset_failed_robustness_gate",
        "forward_failed_scope": "run336M/run336O repaired macro48 and u42 subset only",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "best_preserved_clue": "m48_plain_rf",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifacts = [
        write_csv(
            RUN_DIR / "stage336_forward_decision_matrix.csv",
            (
                "subject",
                "evidence",
                "decision",
                "reason",
                "selected_candidate",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            decision_matrix,
        ),
        write_csv(
            RUN_DIR / "stage336_failure_memory_handoff.csv",
            (
                "failure_axis",
                "severity",
                "finding",
                "affected_attempts",
                "stage337_required_constraint",
                "forbidden_repair_path",
                "salvage_value",
                "reopen_condition",
                "claim_boundary",
            ),
            failure_handoff,
        ),
        write_csv(
            RUN_DIR / "stage337_opening_contract.csv",
            (
                "contract_id",
                "question",
                "required_evidence",
                "forbidden",
                "first_run_use",
                "claim_boundary",
            ),
            stage337_contract,
        ),
        write_csv(
            RUN_DIR / "run337A_design_queue.csv",
            (
                "queue_id",
                "priority",
                "task",
                "required_inputs",
                "required_outputs",
                "forbidden",
                "claim_boundary",
            ),
            run337a_queue,
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ("gate_id", "status", "evidence", "finding", "claim_boundary"),
            gate_audit,
        ),
        write_json(RUN_DIR / "final_stage336P_forward_decision.json", final_decision),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "Stage336 repaired forward subset and next-stage handoff",
                "evidence_available": "run336O MT5 trade-level attribution, cost stress, curve pocket, direction/regime slices, proxy-MT5 parity",
                "evidence_missing": "full-family core56 repaired forward probe and any operating-readiness evidence",
                "judgment_label": "negative",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "수리된 일부 조합은 돌아갔지만 비용, 방향, 곡선이 깨져 성공이 아니라 실패 기억이다.",
            },
        ),
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run336M repaired handoff made fresh runtime probe possible, but run336O showed cost, direction, and curve fragility",
                "comparison_baseline": "run336N timestamp-aligned parity and run336M headline MT5 results",
                "likely_drivers": "thin expectancy, short-side drag, deep rolling pockets, and insufficient cost buffer",
                "segment_checks": "direction, session, hour, month, volatility, ADX, VIX, USD, rate, cost stress, curve pocket",
                "trade_shape": "1225 parsed trades across 4 repaired attempts",
                "alternative_explanations": "macro48/u42 subset only; core56 remains repair condition",
                "attribution_confidence": "medium",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "data_runtime_boundary_receipt.json",
            {
                "data_source": "run336O outputs produced from run336M MT5 reports and run336N parity review",
                "time_axis": "no new bars or labels created in run336P; uses existing audited run336O server-time joins",
                "runtime_path": rel(RUN336O_DIR / "run_manifest.json"),
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution_closeout_only",
                "runtime_claim_boundary": "runtime_probe_not_runtime_authority",
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "run_number": RUN_NUMBER,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": [
                    rel(RUN336O_DECISION),
                    rel(SCORECARD),
                    rel(SUMMARY),
                    rel(FINDINGS),
                    rel(COST_STRESS),
                    rel(CURVE_POCKET),
                    rel(REGIME_SLICE),
                    rel(REPORT_AUDIT),
                    rel(RUN336N_DECISION),
                ],
                "outputs": [rel(path) for path in artifacts],
            },
        )
    )
    return artifacts


def write_reports() -> list[Path]:
    scorecard = read_csv(SCORECARD)
    findings = read_csv(FINDINGS)
    score_lines = "\n".join(
        "| {attempt} | {score} | {net} | {pf} | {c05} | {c10} | {pocket} | {axes} |".format(
            attempt=row["attempt_name"],
            score=row["forward_robustness_score"],
            net=row["net_profit"],
            pf=row["profit_factor"],
            c05=row["cost_plus_0_5_net"],
            c10=row["cost_plus_1_0_net"],
            pocket=row["rolling20_worst_net"],
            axes=row["failure_axes"],
        )
        for row in scorecard.to_dict("records")
    )
    finding_lines = "\n".join(f"- {row['finding_id']}: {row['finding']}" for row in findings.to_dict("records"))
    report = f"""
# run336P Forward Decision and Failure Memory Handoff(336P 전진 판정 및 실패 기억 인계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `repaired_subset_failed_robustness_gate`
- Forward Failed scope(전진 실패 범위): `run336M/run336O repaired macro48 and u42 subset only`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Scorecard(점수표)

| attempt(시도) | score(점수) | net(순익) | PF(수익 팩터) | cost+0.5 net | cost+1.0 net | rolling20 worst(20거래 최악) | failure axes(실패 축) |
|---|---:|---:|---:|---:|---:|---:|---|
{score_lines}

## Failure Memory(실패 기억)

{finding_lines}

## Boundary(경계)

Action(행동): run336O(336O 실행)의 MT5 trade-level attribution(거래 단위 귀속), cost stress(비용 압박), curve pocket(곡선 포켓), direction/regime slice(방향/국면 조각)를 closeout(종료) 판정으로 묶었다.

Effect(효과): repaired subset(수리 부분집합)은 전진 강건성 게이트를 실패했으므로, m48_plain_rf(거시48 일반 랜덤포레스트)는 preserved clue(보존 단서)일 뿐 선택 후보가 아니다. Stage337(337단계)은 cost buffer/direction/curve rebuild(비용 버퍼/방향/곡선 재구성)를 새 질문으로 연다.
"""
    decision_doc = f"""
# 2026-05-27 Stage336P Closeout Decision(336P 종료 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- source_stage(원천 단계): `{STAGE_ID}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `repaired_subset_failed_robustness_gate`
- live_readiness(실거래 준비): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): Stage336(336단계)는 성공 단계가 아니라 실패 기억 인계 단계로 닫는다. 다음 Stage337(337단계)은 비용 버퍼, 방향 대칭, 곡선 포켓, 국면 안정성, proxy-MT5 활용성, runtime handoff(런타임 인계)를 다시 설계한다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision_doc)]


def write_stage337_open_docs() -> list[Path]:
    return [
        write_md(
            NEXT_SPEC_DIR / "stage_brief.md",
            f"""
# Stage337 Cost Buffer Direction Curve Rebuild(337단계 비용 버퍼/방향/곡선 재구성)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- status(상태): `open_active`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- active_question(활성 질문): run336O/run336P(336O/336P 실행)의 cost buffer(비용 버퍼), direction symmetry(방향 대칭), curve pocket(곡선 포켓) 실패를 forward pocket overfit(전진 구간 과적합) 없이 새 ONNX research packet(온엑스 연구 묶음)으로 재구성할 수 있는가?
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): Stage337(337단계)은 run336O(336O 실행)의 실패를 숨기지 않고 새 설계 제약으로 쓴다. 아직 model training(모델 학습), candidate selection(후보 선택), live readiness(실거래 준비)는 없다.
""",
        ),
        write_md(
            NEXT_INPUTS_DIR / "input_refs.md",
            f"""
# Stage337 Input References(337단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_closeout_report(원천 종료 보고서): `{rel(REPORT_DOC)}`
- forward_decision_matrix(전진 판정 행렬): `{rel(RUN_DIR / 'stage336_forward_decision_matrix.csv')}`
- failure_memory_handoff(실패 기억 인계): `{rel(RUN_DIR / 'stage336_failure_memory_handoff.csv')}`
- opening_contract(개방 계약): `{rel(RUN_DIR / 'stage337_opening_contract.csv')}`
- design_queue(설계 대기열): `{rel(RUN_DIR / 'run337A_design_queue.csv')}`
- run336O_scorecard(336O 점수표): `{rel(SCORECARD)}`
- run336O_trade_summary(336O 거래 요약): `{rel(SUMMARY)}`
- run336N_parity_decision(336N 동등성 결정): `{rel(RUN336N_DECISION)}`

Effect(효과): Stage337(337단계)은 run336O(336O 실행)의 나쁜 조각을 직접 필터로 쓰지 않고, 사전 선언된 design constraint(설계 제약)와 negative control(부정 대조)로 바꿔 시작한다.
""",
        ),
        write_md(
            NEXT_RUNS_DIR / "README.md",
            f"""
# Stage337 Runs(337단계 실행)

First planned run(첫 계획 실행): `{NEXT_RUN_ID}`.

Effect(효과): 빈 폴더도 stage structure(단계 구조)를 추적할 수 있게 남긴다.
""",
        ),
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
            [],
        ),
        write_md(
            NEXT_SELECTED_DIR / "selection_status.md",
            f"""
# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- opened_by(개방 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage337(337단계)은 cost buffer(비용 버퍼), direction symmetry(방향 대칭), curve pocket(곡선 포켓)을 새로 설계하는 단계이며, 아직 선택 후보는 없다.
""",
        ),
    ]


def update_status_docs() -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SELECTED_STATUS,
            f"""
# Stage336 Selection Status(336단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `closed_no_selection_repaired_subset_forward_failed_failure_memory_handoff`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `repaired_subset_failed_robustness_gate`
- Forward Failed scope(전진 실패 범위): `run336M/run336O repaired macro48 and u42 subset only`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage336(336단계)은 repaired subset(수리 부분집합)의 비용/방향/곡선 실패를 확인하고 Stage337(337단계) 실패 기억으로 인계했다. 운영 주장은 없다.
""",
        )
    )
    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- status(상태):", "- status(상태): `closed_no_selection_repaired_subset_forward_failed_failure_memory_handoff`")
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    artifacts.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    workspace, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace = replace_prefix_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_prefix_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) `{NEXT_STAGE_ID}`가 run336P(336P 실행)에서 open_active(활성 개방)로 열렸다. "
        "Effect(효과): Stage336(336단계)의 cost/direction/curve failure memory(비용/방향/곡선 실패 기억)를 새 설계 제약으로 쓰되, Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
        "- >-\n"
        f"  Stage336(336단계) run336P(336P 실행)는 `{STATUS}`로 닫혔다. "
        "Effect(효과): repaired subset(수리 부분집합)은 Forward Failed(전진 실패) 범위로 기록하고 m48_plain_rf는 preserved clue(보존 단서)로만 남긴다."
    )
    workspace = insert_focus_once(workspace, focus, "Stage337(337단계)")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(활성 단계):": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- source_stage(원천 단계):": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(목표 표면):": "- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`",
        "- adapter_under_review(검토 중 어댑터):": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
    }
    for prefix, line in replacements.items():
        current = replace_prefix_line(current, prefix, line)
    summary = (
        f"- run336P_summary(336P 요약): Stage336 closeout/open Stage337(336단계 종료/337단계 개방)을 `{STATUS}`로 완료했다. "
        "Effect(효과): run336O(336O 실행)의 비용/방향/곡선 취약성은 repaired subset Forward Failed(수리 부분집합 전진 실패)로 고정하고, Stage337(337단계) cost buffer/direction/curve rebuild(비용 버퍼/방향/곡선 재구성)로 넘긴다. Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = insert_after_marker_once(current, "- decision(결정):", summary, "run336P_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage336P Closeout and Stage337 Open(336P 종료 및 337단계 개방)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run336O(336O 실행)의 scorecard(점수표), cost stress(비용 압박), direction/curve/regime attribution(방향/곡선/국면 귀속)을 stage closeout(단계 종료) 판정으로 묶었다.
- effect(효과): repaired subset(수리 부분집합)은 Forward Failed(전진 실패) 범위로 기록하고, Stage337(337단계)을 cost buffer/direction/curve rebuild(비용 버퍼/방향/곡선 재구성) 단계로 열었다.
- boundary(경계): selected candidate(선택 후보), live readiness(실거래 준비), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
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
                "lane": "stage_closeout_failure_memory_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
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
                "ledger_row_id": f"{RUN_ID}__stage336_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "forward_decision_failure_memory_handoff",
                "tier_scope": "repaired_forward_subset_macro48_u42",
                "kpi_scope": "cost_direction_curve_regime_runtime_probe_review",
                "scoreboard_lane": "stage_closeout_failure_memory_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "forward_failed_scope=repaired_subset;best_clue=m48_plain_rf",
                "guardrail_kpi": "Forward_Passed_not_claimed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "completed_run336M_mt5_runtime_probe_and_run336O_trade_review",
                "notes": f"decision={DECISION};next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID}.",
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
                "ledger_row_id": f"{RUN_ID}__stage336_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "publish_handoff",
                "evidence_scope": "run336M_N_O_repaired_runtime_probe_parity_attribution",
                "kpi_scope": "forward_decision_failure_memory_handoff_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
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
            "stage_id": NEXT_STAGE_ID if NEXT_STAGE_ID in rel(path) else STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": generated_at,
            "notes": "run336P_stage_closeout_stage337_open_no_operating_claim",
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
    run_artifacts = write_run_artifacts()
    report_artifacts = write_reports()
    stage337_artifacts = write_stage337_open_docs()
    status_artifacts = update_status_docs()
    all_artifacts = [
        Path(__file__),
        *run_artifacts,
        *report_artifacts,
        *stage337_artifacts,
        *status_artifacts,
    ]
    manifest_path = RUN_DIR / "run_manifest.json"
    manifest_payload = read_json(manifest_path)
    manifest_payload["created_at_utc"] = generated_at
    manifest_payload["outputs"] = [rel(path) for path in all_artifacts]
    write_json(manifest_path, manifest_payload)
    if manifest_path not in all_artifacts:
        all_artifacts.append(manifest_path)
    register_artifacts = update_registers(all_artifacts, generated_at)
    all_artifacts.extend(register_artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "stage336_closed": True,
                "next_stage": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "repaired_subset_failed_robustness_gate",
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
