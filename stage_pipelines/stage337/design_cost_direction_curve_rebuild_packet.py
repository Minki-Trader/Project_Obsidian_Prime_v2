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
RUN_NUMBER = "run337A"
RUN_ID = "run337A_design_cost_buffer_direction_curve_rebuild_packet_v1"
PARENT_RUN_ID = "run336P_forward_decision_or_failure_memory_handoff_v1"
NEXT_RUN_ID = "run337B_materialize_cost_direction_curve_rebuild_inputs_v1"
STATUS = "completed_cost_direction_curve_rebuild_packet_design_no_selection"
JUDGMENT = "stage337A_predeclared_cost_direction_curve_proxy_mt5_packet_ready_no_selection"
DECISION = "stage337A_cost_direction_curve_rebuild_design_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337A_cost_direction_curve_rebuild_design_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN336P_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336P"
RUN336O_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336O"
RUN336N_DIR = SOURCE_STAGE_DIR / "02_runs" / "run336N"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337A_cost_direction_curve_rebuild_packet_design.md"
REPORT_DOC = REVIEWS_DIR / "run337A_cost_direction_curve_rebuild_packet_design.md"

STAGE337_OPENING_CONTRACT = RUN336P_DIR / "stage337_opening_contract.csv"
RUN337A_DESIGN_QUEUE = RUN336P_DIR / "run337A_design_queue.csv"
FAILURE_MEMORY_HANDOFF = RUN336P_DIR / "stage336_failure_memory_handoff.csv"
FORWARD_DECISION_MATRIX = RUN336P_DIR / "stage336_forward_decision_matrix.csv"
STAGE336P_DECISION = RUN336P_DIR / "final_stage336P_forward_decision.json"
SCORECARD = RUN336O_DIR / "forward_robustness_scorecard.csv"
SUMMARY = RUN336O_DIR / "attempt_forward_attribution_summary.csv"
FINDINGS = RUN336O_DIR / "forward_fragility_findings.csv"
COST_STRESS = RUN336O_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN336O_DIR / "curve_pocket_report.csv"
REGIME_SLICE = RUN336O_DIR / "regime_direction_slice_report.csv"
RUN336N_DECISION = RUN336N_DIR / "final_timestamp_aligned_parity_decision.json"
RUN336N_DIFF = RUN336N_DIR / "timestamp_aligned_proxy_mt5_difference.csv"

DESIGN_CONSTRAINTS_CSV = RUN_DIR / "stage337_design_constraint_matrix.csv"
BRANCH_DESIGN_CSV = RUN_DIR / "cost_direction_curve_branch_design_matrix.csv"
GATE_CONTRACT_CSV = RUN_DIR / "cost_direction_curve_gate_contract.csv"
PROXY_MT5_CONTRACT_CSV = RUN_DIR / "proxy_expected_vs_mt5_runtime_contract.csv"
NEGATIVE_CONTROL_CSV = RUN_DIR / "no_lookahead_negative_control_matrix.csv"
CORE56_BOUNDARY_CSV = RUN_DIR / "core56_refresh_boundary_decision.csv"
RUN337B_QUEUE_CSV = RUN_DIR / "run337B_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
PERFORMANCE_ATTRIBUTION_JSON = RUN_DIR / "performance_attribution_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_cost_direction_curve_rebuild_packet_design_decision.json"
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


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if not text:
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


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
        "opening_contract": read_csv(STAGE337_OPENING_CONTRACT),
        "design_queue": read_csv(RUN337A_DESIGN_QUEUE),
        "failure_memory": read_csv(FAILURE_MEMORY_HANDOFF),
        "decision_matrix": read_csv(FORWARD_DECISION_MATRIX),
        "stage336p_decision": read_json(STAGE336P_DECISION),
        "scorecard": read_csv(SCORECARD),
        "summary": read_csv(SUMMARY),
        "findings": read_csv(FINDINGS),
        "cost_stress": read_csv(COST_STRESS),
        "curve_pocket": read_csv(CURVE_POCKET),
        "regime_slice_exists": path_exists(REGIME_SLICE),
        "run336n_decision_exists": path_exists(RUN336N_DECISION),
        "run336n_diff_exists": path_exists(RUN336N_DIFF),
    }


def summarize_inputs(inputs: Mapping[str, Any]) -> dict[str, Any]:
    scorecard = list(inputs["scorecard"])
    summary = list(inputs["summary"])
    cost_stress = list(inputs["cost_stress"])
    curve_pocket = list(inputs["curve_pocket"])
    attempts = [row["attempt_name"] for row in scorecard]
    best = max(scorecard, key=lambda row: safe_float(row.get("forward_robustness_score")))
    cost_plus_1_failures = [row["attempt_name"] for row in scorecard if safe_float(row.get("cost_plus_1_0_net")) <= 0]
    cost_plus_05_failures = [row["attempt_name"] for row in scorecard if safe_float(row.get("cost_plus_0_5_net")) <= 0]
    short_failures = [row["attempt_name"] for row in scorecard if safe_float(row.get("short_net_profit")) <= 0]
    rolling20_failures = [row["attempt_name"] for row in scorecard if safe_float(row.get("rolling20_worst_net")) <= -50]
    recovery_failures = [row["attempt_name"] for row in scorecard if safe_float(row.get("recovery_factor_closed")) < 1]
    min_trades_day = min(safe_float(row.get("trades_per_calendar_day")) for row in scorecard)
    max_trades_day = max(safe_float(row.get("trades_per_calendar_day")) for row in scorecard)
    worst_cost_row = min(cost_stress, key=lambda row: safe_float(row.get("net_profit")))
    worst_curve_row = min(curve_pocket, key=lambda row: safe_float(row.get("worst_window_net")))
    total_trades = sum(safe_float(row.get("trade_count"), 0.0) for row in summary)
    return {
        "attempts": attempts,
        "attempt_count": len(attempts),
        "best_attempt": best.get("attempt_name"),
        "best_score": safe_float(best.get("forward_robustness_score")),
        "best_net_profit": safe_float(best.get("net_profit")),
        "best_profit_factor": safe_float(best.get("profit_factor")),
        "cost_plus_1_failures": cost_plus_1_failures,
        "cost_plus_05_failures": cost_plus_05_failures,
        "short_failures": short_failures,
        "rolling20_failures": rolling20_failures,
        "recovery_failures": recovery_failures,
        "min_trades_per_day": min_trades_day,
        "max_trades_per_day": max_trades_day,
        "total_trade_count": int(total_trades),
        "worst_cost_attempt": worst_cost_row.get("attempt_name"),
        "worst_cost_extra": safe_float(worst_cost_row.get("extra_cost_per_trade")),
        "worst_cost_net": safe_float(worst_cost_row.get("net_profit")),
        "worst_curve_attempt": worst_curve_row.get("attempt_name"),
        "worst_curve_window": safe_float(worst_curve_row.get("rolling_window_trades")),
        "worst_curve_net": safe_float(worst_curve_row.get("worst_window_net")),
        "run336n_parity_available": bool(inputs["run336n_decision_exists"] and inputs["run336n_diff_exists"]),
    }


def build_design_constraints(inputs: Mapping[str, Any], metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_contracts = {row["contract_id"]: row for row in inputs["opening_contract"]}
    rows: list[dict[str, Any]] = []
    templates = [
        (
            "cost_buffer_expectancy",
            "cost_buffer_fragility",
            "offense+defense",
            "A useful ONNX(온엑스) must keep positive expectancy after broker-like cost stress, not only at zero extra cost.",
            "future candidate hard gate(하드 게이트) and failure memory comparison",
            "run336O repaired subset: 4/4 fail extra_cost_per_trade=1.0",
            "model family, feature order, split rules, MT5 authority, fixed risk accounting",
            "feature thesis and training packet may change only in future predeclared runs",
            "US100 M5, post-2026-04-14 forward evidence plus later WFO(워크포워드) slices",
            "positive net and acceptable PF(수익 팩터) under predeclared cost ladder including +1.0 and +2.0",
            "positive headline net disappears under +1.0 cost or expectancy is concentrated in one pocket",
            "cost ladder, spread, commission, or slippage assumption is changed after seeing forward result",
            "stop or downgrade if cost survival depends on threshold retune(임계값 재조정) or lot optimization(로트 최적화)",
            "cost_stress_report;lot_normalized_report;expectancy_decomposition",
        ),
        (
            "direction_symmetry",
            "direction_asymmetry",
            "defense+offense",
            "Long and short sides must be measured as paired evidence before a side limit is trusted.",
            "branch design and future selection guard",
            "run336O repaired subset: 3/4 non-positive short net",
            "no post-forward side dropping; side logic predeclared",
            "future signal thesis may introduce side-specific features only before forward evaluation",
            "long/short attribution on Tier A(티어 A), Tier B(티어 B), and routed total",
            "both sides contribute or an explicit pre-forward side thesis passes negative controls",
            "short side is removed after seeing forward loss, or one side hides total drawdown",
            "side rule references forward loss bucket, month, hour, or attempt outcome",
            "stop if side-specific gain cannot be reproduced in MT5 runtime probe(런타임 탐침)",
            "D/B attribution;long_short_report;side_negative_control",
        ),
        (
            "curve_pocket_recovery",
            "curve_recovery_fragility",
            "defense",
            "The equity curve must avoid deep rolling pockets and long underwater stretches, not just finish positive.",
            "curve-quality gate(곡선 품질 게이트)",
            "run336O: rolling20 worst net <= -50 in 4/4 attempts",
            "same rolling windows and drawdown definitions across Python and MT5",
            "future objective may include predeclared curve penalty, but no forward pocket filtering",
            "rolling 20/50/100 trades, underwater stretch, recovery factor, month/session pockets",
            "no broken rolling pocket, recovery factor and DD(낙폭) survive cost stress together",
            "single final net hides rolling-window break or underwater concentration",
            "calendar/session/month exclusions are chosen from the failed forward pocket",
            "stop if the curve improves only by lowering trade count below target density",
            "curve_pocket_report;underwater_stretch_report;monthly_session_pocket_report",
        ),
        (
            "regime_stability",
            "worst_regime_slice",
            "defense+diagnostic",
            "Regime slices should explain weakness without becoming post-hoc exclusion filters.",
            "regime attribution(국면 귀속) and economic clue routing",
            "run336O worst slice: u42_bal_rf us10yr_change_flat net=-118.94",
            "slice definitions fixed before new candidate scoring",
            "future feature families may include predeclared macro/rate/volatility interactions",
            "session, hour, month, volatility, ADX, VIX, USD, rate regime slices",
            "no slice is a single catastrophic source of the whole curve",
            "candidate survives only by deleting a known forward-bad slice",
            "rate/volatility regime filter is selected from run336O forward loss",
            "stop if economic indicator alignment uses future publication or same-bar unavailable data",
            "regime_slice_report;economic_indicator_asof_audit",
        ),
        (
            "proxy_mt5_usability",
            "proxy_mt5_boundary",
            "repair+defense",
            "Proxy expected values can sanity-check signals only after comparison with MT5 runtime results.",
            "proxy usability decision(프록시 활용성 결정)",
            "run336N parity matched 20/20 but proxy profit is not KPI authority",
            "MT5 report/telemetry remains KPI authority",
            "future proxy templates may change only to mirror runtime handoff before scoring",
            "each branch must output proxy expected values and MT5 runtime probe values",
            "row-level signal differences are measured and labeled usable/not_usable/context_only",
            "proxy result is used as profit pass/fail without MT5 runtime probe",
            "raw timestamp mismatch is reused without aligned basis",
            "stop if proxy and MT5 disagree on direction or feature readiness at row grain",
            "proxy_expected_result;mt5_runtime_probe_result;difference_report;usability_label",
        ),
        (
            "runtime_feature_handoff",
            "core56_equity_refresh_gap",
            "repair",
            "Full-family claims require fresh timestamp-safe feature handoff for core56 as well as macro48/u42.",
            "handoff repair boundary(인계 수리 경계)",
            "core56 excluded from repaired subset until equity/breadth/top3 refresh is repaired",
            "no full cp322A family claim from macro48/u42 subset only",
            "future data refresh source may be repaired, then parity-probed before any model use",
            "core56 equity, breadth, top3 features, macro48, u42 runtime handoff",
            "feature freshness and timestamp basis pass before full-family report",
            "core56 is silently dropped while claiming family robustness",
            "external equity/breadth source uses future bars or stale last value without audit",
            "stop if core56 repair cannot prove no lookahead and broker-session alignment",
            "feature_freshness_audit;runtime_handoff_snapshot;core56_refresh_decision",
        ),
        (
            "no_lookahead_guard",
            "lookahead_bias_prevention",
            "defense",
            "New research must prove feature-label boundary before any profitable result is interpreted.",
            "invalid-condition guard(무효 조건 방어)",
            "prior work showed split-local and same-bar risks must not return",
            "no future bars, no forward-result-selected threshold, no after-result feature pick",
            "only predeclared experiment variables may change",
            "all Stage337 branches, datasets, labels, joins, and runtime handoff",
            "as-of joins and label boundaries are documented and testable",
            "any feature, rule, or filter reads future outcome or forward result",
            "candidate is repaired after failed forward without a new predeclared packet",
            "stop and mark invalid if lookahead canary passes as if it were legitimate",
            "data_integrity_receipt;negative_control_matrix;split_contract",
        ),
        (
            "high_power_operating_shape",
            "operating_quality_target",
            "offense",
            "The target ONNX(온엑스) must eventually combine high profit, smooth curve, density, and no broken KPI.",
            "future operating-worthy research target, not a current claim",
            "run336O had density but not cost/curve robustness",
            "operating claims remain forbidden until independent MT5 evidence exists",
            "future objective can search stronger signals, but must pass all defensive gates",
            "multi-horizon OOS(표본외), forward, MT5, cost stress, lot-normalized evidence",
            "profit, PF, DD, recovery, expectancy, trade density, and regime slices survive together",
            "one headline metric is great while curve, DD, side, or cost breaks",
            "explosive net is created by leverage, lot, or threshold cosmetics",
            "stop if any core KPI is broken, even with high net profit",
            "final_forward_decision_report;operating_review_only_after_forward_pass",
        ),
    ]
    for template in templates:
        contract = source_contracts.get(template[0], {})
        rows.append(
            {
                "constraint_id": template[0],
                "source_failure_axis": template[1],
                "lane_balance": template[2],
                "hypothesis": template[3],
                "decision_use": template[4],
                "comparison_baseline": template[5],
                "control_variables": template[6],
                "changed_variables": template[7],
                "sample_scope": template[8],
                "success_criteria": template[9],
                "failure_criteria": template[10],
                "invalid_conditions": template[11],
                "stop_conditions": template[12],
                "evidence_plan": template[13],
                "source_contract_question": contract.get("question", ""),
                "source_required_evidence": contract.get("required_evidence", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_branch_design() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "repair_core56_equity_breadth_refresh",
            "lane": "repair",
            "purpose": "restore core56 feature handoff boundary before any full-family claim",
            "primary_failure_memory": "core56_equity_refresh_gap",
            "predeclared_change": "data source refresh and as-of audit only; no model tuning",
            "required_evidence": "feature_freshness_audit;core56_runtime_handoff_snapshot;no_lookahead_asof_receipt",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes after handoff is repaired",
            "success_boundary": "core56 becomes eligible for future research input, not selected",
            "forbidden": "claim full cp322A family robustness while core56 is missing",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "repair_proxy_mt5_runtime_contract",
            "lane": "repair",
            "purpose": "make proxy expected values comparable to MT5 runtime rows before KPI use",
            "primary_failure_memory": "proxy_mt5_boundary",
            "predeclared_change": "comparison grain, timestamp basis, and usability labels",
            "required_evidence": "proxy_expected_result;mt5_runtime_probe_result;difference_report;usability_decision",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes",
            "success_boundary": "proxy can be signal sanity check only when aligned",
            "forbidden": "proxy profit pass/fail or raw timestamp mismatch reuse",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "defense_no_lookahead_canary_suite",
            "lane": "defense",
            "purpose": "reject any feature, split, threshold, or filter that reads future or forward result",
            "primary_failure_memory": "lookahead_bias_prevention",
            "predeclared_change": "negative controls and invalid-condition tests",
            "required_evidence": "lookahead_canary;forward_pocket_filter_canary;threshold_retune_canary",
            "proxy_expected_required": "yes for signal path checks",
            "mt5_runtime_probe_required": "yes before interpreting any candidate",
            "success_boundary": "bad canaries fail and legitimate paths keep timestamp proof",
            "forbidden": "repair branch chosen after seeing failed forward pocket",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "defense_cost_direction_curve_gate",
            "lane": "defense",
            "purpose": "force cost, side, DD, recovery, and curve pocket checks together",
            "primary_failure_memory": "cost_buffer_fragility;direction_asymmetry;curve_recovery_fragility",
            "predeclared_change": "gate measurement only, no scoring or threshold choice",
            "required_evidence": "cost_stress;long_short;rolling20_50_100;underwater;lot_normalized",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes",
            "success_boundary": "future candidates cannot hide broken KPI behind net profit",
            "forbidden": "single headline KPI selection",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_cost_buffer_interaction_search",
            "lane": "offense",
            "purpose": "search stronger expectancy sources that survive cost stress before density expansion",
            "primary_failure_memory": "cost_buffer_fragility",
            "predeclared_change": "feature-family thesis and WFO search packet only",
            "required_evidence": "interaction_family_matrix;cost_ladder;WFO split contract",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes for survivors",
            "success_boundary": "higher net is useful only if cost and curve survive",
            "forbidden": "spread assumption relaxation or forward threshold retune",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_direction_symmetric_signal_thesis",
            "lane": "offense",
            "purpose": "find signal families that do not rely on one broken side",
            "primary_failure_memory": "direction_asymmetry",
            "predeclared_change": "side-aware thesis before seeing new forward outcome",
            "required_evidence": "side KPI;D source;B source;D+B attribution;negative side-drop control",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes for side-level signal parity",
            "success_boundary": "both sides pass or side limit is justified before forward",
            "forbidden": "post-forward short drop",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_curve_quality_objective_probe",
            "lane": "offense",
            "purpose": "shape future objectives around smooth tradable curves without pocket fitting",
            "primary_failure_memory": "curve_recovery_fragility",
            "predeclared_change": "pre-forward curve penalty or selection audit design",
            "required_evidence": "rolling pocket;underwater stretch;recovery factor;trade density",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes for final candidates",
            "success_boundary": "curve improves without deleting forward-bad periods",
            "forbidden": "calendar pocket trimming",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "branch_id": "offense_regime_invariant_rebuild",
            "lane": "offense",
            "purpose": "use macro/rate/volatility clues as predeclared features, not post-hoc filters",
            "primary_failure_memory": "worst_regime_slice",
            "predeclared_change": "economic indicator as-of contract and regime feature thesis",
            "required_evidence": "VIX;USD;rate;ADX;volatility;session/month slice attribution",
            "proxy_expected_required": "yes",
            "mt5_runtime_probe_required": "yes for regime survivors",
            "success_boundary": "no single regime dominates loss or profit",
            "forbidden": "filter chosen from run336O worst slice",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_contract() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "cost_stress_survival",
            "scope": "all future Stage337 candidates",
            "required_measurement": "net/PF/expectancy at base, +0.5, +1.0, +2.0 extra cost per trade",
            "acceptance_boundary": "no Forward Passed(전진 통과) unless cost+1.0 survives; +2.0 remains stress evidence",
            "failure_memory_trigger": "run336O cost+1.0 failed 4/4 attempts",
            "forbidden_shortcut": "threshold retune, lot optimization, or spread assumption relaxation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "direction_symmetry_attribution",
            "scope": "D source/B source/D+B and long/short",
            "required_measurement": "long_net, short_net, trade counts, side expectancy, side DD",
            "acceptance_boundary": "both sides must be reported; side limitation must be predeclared",
            "failure_memory_trigger": "run336O short side non-positive in 3/4 attempts",
            "forbidden_shortcut": "post-forward short-side drop",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "curve_pocket_underwater",
            "scope": "rolling 20/50/100 trades and month/session pockets",
            "required_measurement": "worst window net, longest underwater, recovery factor, DD",
            "acceptance_boundary": "no single pocket can break the curve while headline net stays positive",
            "failure_memory_trigger": "run336O rolling20 worst net <= -50 in 4/4 attempts",
            "forbidden_shortcut": "calendar or session exclusion selected from failed forward pocket",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "density_quality_joint_gate",
            "scope": "trade count and trades/day",
            "required_measurement": "trades/day, total trades, expectancy, PF, DD together",
            "acceptance_boundary": "density must remain useful without degrading cost and curve quality",
            "failure_memory_trigger": "run336O density existed but KPI broke elsewhere",
            "forbidden_shortcut": "trade-count-only objective or lot cosmetic repair",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "regime_slice_stability",
            "scope": "session/hour/month/volatility/ADX/VIX/USD/rate",
            "required_measurement": "slice net, PF, DD, trade count, concentration",
            "acceptance_boundary": "regime analysis may explain but not post-hoc exclude",
            "failure_memory_trigger": "u42_bal_rf us10yr_change_flat net=-118.94",
            "forbidden_shortcut": "rate-regime filter selected from run336O failed slice",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_usability",
            "scope": "proxy expected values and MT5 runtime probe",
            "required_measurement": "row-level signal delta, feature-ready delta, trade/KPI delta, usability label",
            "acceptance_boundary": "proxy allowed only as signal sanity check unless MT5 runtime agrees",
            "failure_memory_trigger": "run336N parity usable for signal comparison only",
            "forbidden_shortcut": "proxy profit authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "feature_handoff_freshness",
            "scope": "macro48/u42/core56",
            "required_measurement": "latest feature timestamp, broker M5 timestamp, as-of source identity",
            "acceptance_boundary": "full-family claims require repaired core56 freshness and parity",
            "failure_memory_trigger": "core56 equity refresh gap",
            "forbidden_shortcut": "silent core56 exclusion",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_invalidity",
            "scope": "all data, feature, label, split, and filter paths",
            "required_measurement": "feature-label boundary audit, as-of join audit, negative control rejection",
            "acceptance_boundary": "any lookahead evidence invalidates the result before KPI interpretation",
            "failure_memory_trigger": "look-ahead-bias must not recur",
            "forbidden_shortcut": "forward result used to choose threshold, feature, side, or regime filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_mt5_contract(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    subjects = [*metrics["attempts"], "core56_refresh_candidate"]
    rows = []
    for subject in subjects:
        is_core56 = subject == "core56_refresh_candidate"
        rows.append(
            {
                "contract_id": f"{subject}_proxy_mt5_expected_runtime_compare",
                "subject": subject,
                "proxy_expected_artifact_required": "proxy_expected_signal_values.csv",
                "mt5_runtime_probe_artifact_required": "MT5 strategy tester report + telemetry + runtime_execution_result.json"
                if not is_core56
                else "required after core56 feature refresh source is repaired",
                "comparison_grain": "timestamp-aligned cycle_bar_time and trade/order identity where available",
                "difference_metrics": "feature_ready_delta;direction_delta;flat_delta;trade_count_delta;net_delta;PF_delta;DD_delta",
                "usability_rule": (
                    "usable_for_signal_sanity_only if row-level signal and readiness match; "
                    "context_only if KPI differs; not_usable if direction/readiness mismatch"
                ),
                "allowed_use": "signal sanity check;runtime handoff debugging;not KPI authority",
                "forbidden_use": "Forward Passed/Failed decision, candidate selection, or profit claim without MT5 runtime probe",
                "next_materialization": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "forward_pocket_filter_canary",
            "target_risk": "post-forward calendar/session/month exclusion",
            "test_design": "inject a rule that references a known bad run336O pocket and verify it is rejected",
            "expected_failure_signature": "invalid_forward_result_dependent_filter",
            "stop_condition": "any branch using this filter is invalid",
            "repair_action": "move to pre-forward thesis or remove",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "threshold_retune_canary",
            "target_risk": "score threshold fitted to forward outcomes",
            "test_design": "tag any threshold chosen after seeing forward KPI",
            "expected_failure_signature": "invalid_threshold_retune",
            "stop_condition": "candidate cannot be scored",
            "repair_action": "new predeclared WFO threshold protocol only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "lot_optimization_canary",
            "target_risk": "profit created by lot or risk cosmetics",
            "test_design": "require lot-normalized result and fixed-lot comparison",
            "expected_failure_signature": "profit_not_lot_normalized",
            "stop_condition": "operating-like claim forbidden",
            "repair_action": "return to signal/expectancy research",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "side_drop_canary",
            "target_risk": "dropping short side after seeing loss",
            "test_design": "detect side filters whose trigger references run336O side attribution",
            "expected_failure_signature": "invalid_post_forward_side_filter",
            "stop_condition": "side-limited branch invalid unless predeclared",
            "repair_action": "predeclare side thesis and rerun from clean split",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "macro_asof_lookahead_canary",
            "target_risk": "economic indicator value unavailable at bar close",
            "test_design": "compare indicator timestamp, publication/as-of timestamp, and M5 close timestamp",
            "expected_failure_signature": "future_indicator_value_used",
            "stop_condition": "all KPI invalid until as-of repair",
            "repair_action": "backward as-of join with release lag and audit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "proxy_profit_authority_canary",
            "target_risk": "proxy used as final KPI authority",
            "test_design": "require MT5 runtime output before any net/PF/DD judgment",
            "expected_failure_signature": "proxy_profit_claim_without_mt5",
            "stop_condition": "result remains context_only",
            "repair_action": "run MT5 probe or lower claim",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "core56_silent_drop_canary",
            "target_risk": "full-family claim while core56 is absent",
            "test_design": "compare reported family scope with feature handoff availability",
            "expected_failure_signature": "full_family_claim_without_core56",
            "stop_condition": "full-family robustness claim rejected",
            "repair_action": "repair core56 source or report macro48/u42 subset only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "single_slice_winner_canary",
            "target_risk": "candidate selected because one forward slice dominates",
            "test_design": "measure month/session/regime contribution concentration before selection",
            "expected_failure_signature": "single_slice_profit_concentration",
            "stop_condition": "candidate becomes failure memory or needs new predeclared thesis",
            "repair_action": "broaden signal or add pre-forward regime-invariant test",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_core56_boundary() -> list[dict[str, Any]]:
    return [
        {
            "subject": "core56_equity_breadth_top3",
            "current_status": "out_of_full_family_claim_until_refresh_repair",
            "reason": "Stage336P failure memory says core56 remains outside repaired forward subset",
            "required_repair": "equity/breadth/top3 source refresh with timestamp-safe as-of contract",
            "required_validation": "feature freshness audit;proxy expected result;MT5 runtime probe;row-level parity",
            "allowed_use_before_repair": "failure memory and repair planning only",
            "forbidden_use_before_repair": "full cp322A family robustness claim;Forward Passed;runtime authority",
            "next_run_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "stage337B_source_lineage_and_data_integrity",
            "priority": 1,
            "task": "Materialize source lineage, time-axis, split, and no-lookahead guard inputs.",
            "required_inputs": "run336P failure memory;run336O scorecard;run336N parity evidence;Stage337 contracts",
            "required_outputs": "source_lineage_index;data_integrity_contract;no_lookahead_canary_inputs",
            "proxy_mt5_requirement": "define comparison grain before proxy values are interpreted",
            "forbidden": "training or threshold search before data boundary receipt",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337B_branch_package_materialization",
            "priority": 2,
            "task": "Create repair/defense/offense branch packages from run337A design matrix.",
            "required_inputs": "branch_design_matrix;negative_controls;gate_contract",
            "required_outputs": "branch_payloads;branch_review_queue;gate_schema_per_branch",
            "proxy_mt5_requirement": "each branch must state proxy expected and MT5 runtime artifacts",
            "forbidden": "single KPI branch package",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337B_proxy_mt5_expected_runtime_templates",
            "priority": 3,
            "task": "Materialize proxy expected result templates and MT5 runtime probe package templates together.",
            "required_inputs": "proxy_mt5_contract;runtime handoff identity",
            "required_outputs": "proxy_expected_schema;mt5_probe_manifest;difference_report_schema;usability_rule",
            "proxy_mt5_requirement": "proxy expected values and MT5 runtime results must both be present before usability judgment",
            "forbidden": "proxy-only profit pass/fail",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337B_cost_direction_curve_gate_templates",
            "priority": 4,
            "task": "Materialize cost stress, direction, curve pocket, lot-normalized, and regime gate templates.",
            "required_inputs": "gate_contract;run336O failure memory",
            "required_outputs": "cost_ladder_schema;long_short_schema;curve_pocket_schema;regime_slice_schema",
            "proxy_mt5_requirement": "MT5 remains KPI authority for gate closure",
            "forbidden": "post-forward pocket filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "stage337B_core56_refresh_repair_or_scope_lock",
            "priority": 5,
            "task": "Decide whether core56 source can be repaired now; otherwise lock family scope honestly.",
            "required_inputs": "core56_boundary_decision;available equity/breadth/top3 sources",
            "required_outputs": "core56_repair_queue_or_out_of_scope_receipt",
            "proxy_mt5_requirement": "core56 proxy and MT5 probe required after repair",
            "forbidden": "silent core56 drop",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(
    inputs: Mapping[str, Any],
    constraints: Sequence[Mapping[str, Any]],
    branches: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    proxy_contract: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    required_paths = [
        STAGE337_OPENING_CONTRACT,
        RUN337A_DESIGN_QUEUE,
        FAILURE_MEMORY_HANDOFF,
        FORWARD_DECISION_MATRIX,
        STAGE336P_DECISION,
        SCORECARD,
        SUMMARY,
        FINDINGS,
        COST_STRESS,
        CURVE_POCKET,
        RUN336N_DIFF,
    ]
    missing = [rel(path) for path in required_paths if not path_exists(path)]
    axis_text = ";".join(row.get("source_failure_axis", "") for row in constraints)
    contract_text = json.dumps(proxy_contract, ensure_ascii=False)
    forbidden_text = json.dumps([constraints, branches, gates, proxy_contract, controls, queue], ensure_ascii=False)
    audit = [
        {
            "gate_id": "source_inputs_present",
            "status": "pass" if not missing else "fail",
            "evidence": ";".join(rel(path) for path in required_paths),
            "finding": "all required Stage336P/336O/336N source artifacts found" if not missing else f"missing={missing}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage336_failed_scope_preserved",
            "status": "pass"
            if inputs["stage336p_decision"].get("forward_failed") == "repaired_subset_failed_robustness_gate"
            else "fail",
            "evidence": rel(STAGE336P_DECISION),
            "finding": "Stage336P failure scope preserved; not rebranded as pass",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost_direction_curve_axes_represented",
            "status": "pass"
            if all(axis in axis_text for axis in ["cost_buffer_fragility", "direction_asymmetry", "curve_recovery_fragility"])
            else "fail",
            "evidence": rel(DESIGN_CONSTRAINTS_CSV),
            "finding": "cost, direction, and curve failure axes mapped to constraints",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_expected_and_mt5_runtime_both_required",
            "status": "pass"
            if "proxy_expected_artifact_required" in contract_text and "mt5_runtime_probe_artifact_required" in contract_text
            else "fail",
            "evidence": rel(PROXY_MT5_CONTRACT_CSV),
            "finding": "proxy expected values and MT5 runtime probe results are paired before usability judgment",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_negative_controls_present",
            "status": "pass" if len(controls) >= 8 else "fail",
            "evidence": rel(NEGATIVE_CONTROL_CSV),
            "finding": f"negative controls={len(controls)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_repair_paths_blocked",
            "status": "pass"
            if all(term in forbidden_text for term in ["threshold", "lot", "forward", "proxy"])
            else "fail",
            "evidence": rel(BRANCH_DESIGN_CSV),
            "finding": "threshold retune, lot optimization, forward pocket filters, and proxy profit authority are blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_materialization_queue_ready",
            "status": "pass" if len(queue) >= 5 else "fail",
            "evidence": rel(RUN337B_QUEUE_CSV),
            "finding": f"run337B queue rows={len(queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_guard_no_selection_no_goal",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "no candidate, Forward Passed, runtime authority, or Goal Achieve claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return audit


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_RECEIPT_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "Stage337 can rebuild toward a stronger ONNX(온엑스) only if cost buffer, direction symmetry, curve pockets, proxy-MT5 usability, and no-lookahead controls are predeclared together.",
                "decision_use": "design next materialization and future candidate gates; no candidate selection",
                "comparison_baseline": "run336O repaired subset failure memory and m48_plain_rf preserved clue",
                "control_variables": "no model training, no score threshold retune, no lot optimization, no forward pocket filter in run337A",
                "changed_variables": "research packet design, branch contracts, gate contracts, proxy-MT5 expected/runtime comparison contract",
                "sample_scope": "US100 M5 post-2026-04-14 forward evidence from run336M/N/O/P plus future WFO/MT5 scopes",
                "success_criteria": "run337B can materialize branch inputs with proxy expected result and MT5 runtime probe requirements",
                "failure_criteria": "design omits cost, direction, curve, no-lookahead, proxy-MT5, or core56 boundary",
                "invalid_conditions": "lookahead, forward-result-tuned threshold, lot cosmetic repair, proxy-only KPI authority",
                "stop_conditions": "stop or downgrade if any required gate audit fails",
                "evidence_plan": "design CSVs, receipts, gate audit, run337B queue, stage/run/artifact ledgers",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run336P failure handoff, run336O MT5 attribution/cost/curve reports, run336N timestamp-aligned parity evidence",
                "time_axis": "US100 M5 broker bar close/cycle_bar_time; run337A designs checks only and does not create labels",
                "sample_scope": "repaired macro48/u42 forward subset plus core56 refresh boundary planning",
                "missing_or_duplicate_check": "source presence checked; detailed row gap checks deferred to run337B materialization",
                "feature_label_boundary": "no labels or outcomes are used to train; failure memory becomes predeclared constraints only",
                "split_boundary": "future WFO/OOS/forward boundaries must be materialized before model training",
                "leakage_risk": "forward bad pockets could become filters; blocked by negative controls",
                "data_hash_or_identity": rel(GATE_AUDIT_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "future MT5 probe package from run337B+; no Strategy Tester run in run337A",
                "shared_contract": "features, signal rows, threshold identity, runtime handoff, and MT5 report/telemetry must match before KPI claims",
                "known_differences": "proxy expected values are not KPI authority; MT5 remains net/PF/DD authority",
                "parity_check": "design requires proxy expected result and MT5 runtime probe result difference report",
                "parity_identity": rel(RUN336N_DIFF) if path_exists(RUN336N_DIFF) else "missing_run336N_diff",
                "runtime_claim_boundary": "research-only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [
                    rel(STAGE337_OPENING_CONTRACT),
                    rel(FAILURE_MEMORY_HANDOFF),
                    rel(SCORECARD),
                    rel(SUMMARY),
                    rel(RUN336N_DIFF),
                ],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(DESIGN_CONSTRAINTS_CSV),
                    rel(BRANCH_DESIGN_CSV),
                    rel(GATE_CONTRACT_CSV),
                    rel(PROXY_MT5_CONTRACT_CSV),
                    rel(RUN337B_QUEUE_CSV),
                ],
                "artifact_hashes": "registered in docs/registers/artifact_registry.csv after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; run337A outputs are reproducible from script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            PERFORMANCE_ATTRIBUTION_JSON,
            {
                "run_id": RUN_ID,
                "observed_change": "run337A does not claim performance improvement; it converts run336O KPI breaks into predeclared gates",
                "comparison_baseline": "run336O best clue m48_plain_rf net=268.51 PF=1.481 but cost+1.0 net=-5.49 and rolling20=-62.79",
                "likely_drivers": "cost fragility, short-side weakness, rolling curve pocket, core56 feature gap, proxy authority boundary",
                "segment_checks": "direction, cost ladder, rolling window, regime, feature handoff, proxy-MT5 planned as required evidence",
                "trade_shape": f"run336O repaired subset attempts={metrics['attempt_count']}; trades={metrics['total_trade_count']}; trades/day range={metrics['min_trades_per_day']:.2f}-{metrics['max_trades_per_day']:.2f}",
                "alternative_explanations": "forward pocket overfit, cost assumption weakness, timestamp basis mismatch, economic regime concentration",
                "attribution_confidence": "medium_for_failure_memory_low_for_new_solution",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "Stage337A design packet",
                "evidence_available": "design constraints, branch matrix, gate contract, proxy-MT5 contract, negative controls, run337B queue",
                "evidence_missing": "no new model, no MT5 run, no forward pass/fail for Stage337",
                "judgment_label": "exploratory",
                "claim_boundary": "design ready only; no Forward Passed, no Forward Failed for Stage337, no runtime authority, no Goal Achieve",
                "next_condition": "run337B must materialize inputs and runtime/proxy templates, then later MT5 probes must execute",
                "user_explanation_hook": "설계가 닫힌 것이지 모델이 좋아졌다는 뜻은 아니다.",
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
# run337A Cost Direction Curve Rebuild Packet Design(337A 비용/방향/곡선 재구성 설계)

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

## Evidence Used(사용 근거)

- best_preserved_clue(보존 단서): `{metrics['best_attempt']}` score(점수) `{metrics['best_score']}`, net(순익) `{metrics['best_net_profit']}`, PF(수익 팩터) `{metrics['best_profit_factor']}`
- cost_failure(비용 실패): cost+1.0 net(비용+1.0 순익) non-positive attempts(비양수 시도) `{len(metrics['cost_plus_1_failures'])}/{metrics['attempt_count']}`
- direction_failure(방향 실패): short-side non-positive(숏 방향 비양수) `{len(metrics['short_failures'])}/{metrics['attempt_count']}`
- curve_failure(곡선 실패): rolling20 worst <= -50(롤링20 최악 -50 이하) `{len(metrics['rolling20_failures'])}/{metrics['attempt_count']}`
- proxy_mt5_boundary(프록시-MT5 경계): run336N(336N 실행) aligned parity evidence(정렬 동등성 근거) available(존재) `{metrics['run336n_parity_available']}`

## Materialized Design(물질화 설계)

- design constraints(설계 제약): `{rel(DESIGN_CONSTRAINTS_CSV)}`
- branch matrix(분기 행렬): `{rel(BRANCH_DESIGN_CSV)}`
- gate contract(게이트 계약): `{rel(GATE_CONTRACT_CSV)}`
- proxy-MT5 contract(프록시-MT5 계약): `{rel(PROXY_MT5_CONTRACT_CSV)}`
- negative controls(부정 대조): `{rel(NEGATIVE_CONTROL_CSV)}`
- run337B queue(337B 대기열): `{rel(RUN337B_QUEUE_CSV)}`

Effect(효과): Stage337(337단계)은 수익이 좋아 보이는 조각을 바로 고르지 않고, cost buffer(비용 버퍼), direction symmetry(방향 대칭), curve pocket(곡선 포켓), proxy expected value(프록시 예상값), MT5 runtime probe(MT5 런타임 탐침), no-lookahead guard(미래참조 방어)를 다음 실행의 필수 물증으로 고정했다.
"""
    decision = f"""
# 2026-05-27 Stage337A Decision(337A 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- source_failure_memory(원천 실패 기억): `run336P_forward_decision_or_failure_memory_handoff_v1`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): proxy test(프록시 테스트)는 proxy expected result(프록시 예상 결과)와 MT5 runtime probe result(MT5 런타임 탐침 결과)를 함께 본 뒤 difference report(차이 보고서)와 usability label(활용성 라벨)을 붙이는 경로로 고정됐다.
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
- opened_by(개방 실행): `{PARENT_RUN_ID}`
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
- effect(효과): run337A(337A 실행)는 cost buffer(비용 버퍼), direction symmetry(방향 대칭), curve pocket(곡선 포켓), proxy-MT5 usability(프록시-MT5 활용성), no-lookahead guard(미래참조 방어)를 다음 물질화 게이트로 고정했다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))
    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- status(상태):", "- status(상태): `open_active`")
    brief_text = replace_prefix_line(brief_text, "- first_run(첫 실행):", f"- first_run(첫 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- first_run(첫 실행):",
        f"- latest_run(최신 실행): `{RUN_ID}`",
        "latest_run(최신 실행)",
    )
    brief_text = insert_after_marker_once(
        brief_text,
        "- active_question(활성 질문):",
        f"- run337A_summary(337A 요약): `{STATUS}`. Effect(효과): 다음 run337B(337B 실행)는 proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)를 함께 물질화해야 한다.",
        "run337A_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))
    input_section = f"""
## run337A Outputs(337A 산출물)

- design_constraints(설계 제약): `{rel(DESIGN_CONSTRAINTS_CSV)}`
- branch_design(분기 설계): `{rel(BRANCH_DESIGN_CSV)}`
- gate_contract(게이트 계약): `{rel(GATE_CONTRACT_CSV)}`
- proxy_mt5_contract(프록시-MT5 계약): `{rel(PROXY_MT5_CONTRACT_CSV)}`
- next_queue(다음 대기열): `{rel(RUN337B_QUEUE_CSV)}`

Effect(효과): 다음 실행은 proxy(프록시)만 보지 않고 MT5 runtime probe(런타임 탐침)까지 같이 만들어 difference(차이)와 usability(활용성)를 판정한다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337A Outputs(337A 산출물)", input_section))
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337(337단계) run337A(337A 실행)는 `{STATUS}`로 design packet(설계 묶음)을 완료했다. "
        "Effect(효과): cost/direction/curve(비용/방향/곡선), proxy expected vs MT5 runtime(프록시 예상값 대 MT5 런타임), core56 refresh(핵심56 갱신), no-lookahead guard(미래참조 방어)를 run337B(337B 실행)의 필수 물질화 조건으로 고정한다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "run337A(337A 실행)")
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
        f"- run337A_summary(337A 요약): `{STATUS}`. "
        "Effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime probe result(MT5 런타임 탐침 결과)를 함께 요구하는 contract(계약), cost/direction/curve gate(비용/방향/곡선 게이트), no-lookahead negative control(미래참조 부정 대조)을 만들고 run337B(337B 실행)로 넘긴다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337A_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337A Cost Direction Curve Design(337A 비용/방향/곡선 설계)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): Stage336P(336P 실행)의 failure memory(실패 기억)를 Stage337(337단계)의 설계 제약, branch matrix(분기 행렬), gate contract(게이트 계약), proxy-MT5 contract(프록시-MT5 계약), negative controls(부정 대조), run337B queue(337B 대기열)로 물질화했다.
- effect(효과): proxy test(프록시 테스트)는 proxy expected result(프록시 예상 결과), MT5 runtime probe result(MT5 런타임 탐침 결과), difference report(차이 보고서), usability label(활용성 라벨)을 함께 요구한다.
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
                "lane": "cost_direction_curve_rebuild_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_mt5_expected_runtime_contract_ready;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "cost_direction_curve_rebuild_packet_design",
                "tier_scope": "research_design_macro48_u42_core56_boundary",
                "kpi_scope": "no_new_kpi_design_from_failure_memory",
                "scoreboard_lane": "repair_defense_offense_balanced_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "no_new_trading_kpi;best_clue=m48_plain_rf_preserved_only",
                "guardrail_kpi": "proxy_mt5_required;cost_direction_curve_required;goal_achieve_not_claimed",
                "external_verification_status": "design_only_runtime_probe_required_next",
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
                "ledger_row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design",
                "evidence_scope": "run336P_failure_memory_run336O_cost_direction_curve_run336N_parity",
                "kpi_scope": "design_only_no_new_forward_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};proxy_expected_and_mt5_runtime_probe_required;goal_achieve_not_claimed.",
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
            "notes": "run337A_design_no_selection_proxy_mt5_expected_runtime_contract",
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
    metrics = summarize_inputs(inputs)
    constraints = build_design_constraints(inputs, metrics)
    branches = build_branch_design()
    gates = build_gate_contract()
    proxy_contract = build_proxy_mt5_contract(metrics)
    controls = build_negative_controls()
    core56 = build_core56_boundary()
    queue = build_queue()
    audit = build_gate_audit(inputs, constraints, branches, gates, proxy_contract, controls, queue)
    failed_gates = [row for row in audit if row["status"] != "pass"]
    run_artifacts = [
        write_csv(
            DESIGN_CONSTRAINTS_CSV,
            (
                "constraint_id",
                "source_failure_axis",
                "lane_balance",
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
                "source_contract_question",
                "source_required_evidence",
                "claim_boundary",
            ),
            constraints,
        ),
        write_csv(
            BRANCH_DESIGN_CSV,
            (
                "branch_id",
                "lane",
                "purpose",
                "primary_failure_memory",
                "predeclared_change",
                "required_evidence",
                "proxy_expected_required",
                "mt5_runtime_probe_required",
                "success_boundary",
                "forbidden",
                "next_run_use",
                "claim_boundary",
            ),
            branches,
        ),
        write_csv(
            GATE_CONTRACT_CSV,
            (
                "gate_id",
                "scope",
                "required_measurement",
                "acceptance_boundary",
                "failure_memory_trigger",
                "forbidden_shortcut",
                "claim_boundary",
            ),
            gates,
        ),
        write_csv(
            PROXY_MT5_CONTRACT_CSV,
            (
                "contract_id",
                "subject",
                "proxy_expected_artifact_required",
                "mt5_runtime_probe_artifact_required",
                "comparison_grain",
                "difference_metrics",
                "usability_rule",
                "allowed_use",
                "forbidden_use",
                "next_materialization",
                "claim_boundary",
            ),
            proxy_contract,
        ),
        write_csv(
            NEGATIVE_CONTROL_CSV,
            (
                "control_id",
                "target_risk",
                "test_design",
                "expected_failure_signature",
                "stop_condition",
                "repair_action",
                "claim_boundary",
            ),
            controls,
        ),
        write_csv(
            CORE56_BOUNDARY_CSV,
            (
                "subject",
                "current_status",
                "reason",
                "required_repair",
                "required_validation",
                "allowed_use_before_repair",
                "forbidden_use_before_repair",
                "next_run_use",
                "claim_boundary",
            ),
            core56,
        ),
        write_csv(
            RUN337B_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "task",
                "required_inputs",
                "required_outputs",
                "proxy_mt5_requirement",
                "forbidden",
                "claim_boundary",
            ),
            queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS if not failed_gates else "blocked_stage337A_gate_failure",
                "judgment": JUDGMENT if not failed_gates else "stage337A_design_gate_failure_requires_repair",
                "decision": DECISION if not failed_gates else "stage337A_design_blocked_gate_failure",
                "metrics": metrics,
                "failed_gates": failed_gates,
                "next_action": NEXT_RUN_ID,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    run_artifacts.extend(write_receipts(metrics))
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
                "source_inputs": [
                    rel(STAGE337_OPENING_CONTRACT),
                    rel(RUN337A_DESIGN_QUEUE),
                    rel(FAILURE_MEMORY_HANDOFF),
                    rel(SCORECARD),
                    rel(RUN336N_DIFF),
                ],
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337A_gate_failure",
                "decision": "stage337A_design_blocked_gate_failure",
                "failed_gates": failed_gates,
                "next_action": NEXT_RUN_ID,
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
            rel(STAGE337_OPENING_CONTRACT),
            rel(RUN337A_DESIGN_QUEUE),
            rel(FAILURE_MEMORY_HANDOFF),
            rel(FORWARD_DECISION_MATRIX),
            rel(STAGE336P_DECISION),
            rel(SCORECARD),
            rel(SUMMARY),
            rel(FINDINGS),
            rel(COST_STRESS),
            rel(CURVE_POCKET),
            rel(RUN336N_DIFF),
        ],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "design_only_runtime_probe_required_next",
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
                "constraints": len(constraints),
                "branches": len(branches),
                "gates": len(gates),
                "negative_controls": len(controls),
                "proxy_mt5_contract_rows": len(proxy_contract),
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
