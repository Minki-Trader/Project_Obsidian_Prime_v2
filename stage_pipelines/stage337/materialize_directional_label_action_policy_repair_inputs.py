from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    replace_bullet_value,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    sha256_file,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
    now_utc,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CH"
RUN_ID = "run337CH_materialize_directional_label_action_policy_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337CG_design_directional_label_action_policy_repair_without_db_v1"
NEXT_RUN_ID = "run337CI_review_directional_label_action_policy_repair_inputs_without_db_v1"
STATUS = "completed_stage337CH_directional_label_action_policy_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "polarity_label_action_repair_inputs_materialized_with_no_forward_selection_firewall"
DECISION = "stage337CH_open_run337CI_review_directional_label_action_policy_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CH_directional_label_action_policy_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
CG_DIR = STAGE_DIR / "02_runs" / "run337CG"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CH_directional_label_action_policy_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CH_directional_label_action_policy_repair_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CG_FINAL = CG_DIR / "final_decision.json"
CG_DESIGN = CG_DIR / "directional_label_action_repair_design_matrix.csv"
CG_LABEL = CG_DIR / "label_policy_repair_contract.csv"
CG_ACTION = CG_DIR / "action_policy_repair_contract.csv"
CG_PROTOCOL = CG_DIR / "no_overfit_validation_protocol.csv"
CG_PROXY = CG_DIR / "proxy_mt5_usability_policy.csv"
CG_QUEUE = CG_DIR / "run337CH_materialization_queue.csv"

POLARITY_AUDIT = RUN_DIR / "polarity_audit_plan.csv"
LABEL_V3_INPUT = RUN_DIR / "label_v3_input_contract.csv"
ACTION_V3_INPUT = RUN_DIR / "action_v3_input_contract.csv"
NEGATIVE_CONTROL = RUN_DIR / "negative_control_plan.csv"
FORWARD_FIREWALL = RUN_DIR / "forward_selection_firewall.csv"
RUNTIME_REQUIREMENT = RUN_DIR / "runtime_probe_requirement.csv"
CURVE_QUALITY_PLAN = RUN_DIR / "curve_quality_measurement_plan.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
NEXT_QUEUE = RUN_DIR / "run337CI_review_queue.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (CG_FINAL, CG_DESIGN, CG_LABEL, CG_ACTION, CG_PROTOCOL, CG_PROXY, CG_QUEUE)
OUTPUT_FILES = (
    POLARITY_AUDIT,
    LABEL_V3_INPUT,
    ACTION_V3_INPUT,
    NEGATIVE_CONTROL,
    FORWARD_FIREWALL,
    RUNTIME_REQUIREMENT,
    CURVE_QUALITY_PLAN,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    NEXT_QUEUE,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

POLARITY_COLUMNS = (
    "audit_id",
    "source_contract",
    "original_diagnostic",
    "flipped_diagnostic",
    "split_scope",
    "cost_ladder",
    "negative_control",
    "selection_rule",
    "invalid_if",
    "effect",
    "claim_boundary",
)
LABEL_INPUT_COLUMNS = (
    "label_input_id",
    "label_policy_id",
    "source_fields",
    "time_axis",
    "sample_scope",
    "target_formula_template",
    "cost_buffer",
    "split_policy",
    "forbidden_shortcut",
    "required_outputs",
    "claim_boundary",
)
ACTION_INPUT_COLUMNS = (
    "action_input_id",
    "action_policy_id",
    "required_score_inputs",
    "entry_template",
    "exit_template",
    "density_floor",
    "attribution_required",
    "risk_fixed",
    "forbidden_shortcut",
    "required_outputs",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_family",
    "procedure",
    "expected_behavior",
    "blocks_if",
    "split_scope",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "forbidden_source",
    "forbidden_decision",
    "allowed_use",
    "evidence_output",
    "blocks_claim",
    "effect",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "requirement_id",
    "required_artifact",
    "compare_fields",
    "acceptance_rule",
    "tester_gap_rule",
    "blocks_claim",
    "effect",
    "claim_boundary",
)
CURVE_COLUMNS = (
    "metric_id",
    "metric_family",
    "required_slice",
    "minimum_evidence",
    "failure_signal",
    "blocks_claim",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def summarize_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    final = read_json(CG_FINAL)
    design_rows = read_csv(CG_DESIGN)
    label_rows = read_csv(CG_LABEL)
    action_rows = read_csv(CG_ACTION)
    protocol_rows = read_csv(CG_PROTOCOL)
    proxy_rows = read_csv(CG_PROXY)
    queue_rows = read_csv(CG_QUEUE)
    return {
        "missing_inputs": missing,
        "cg_final": final,
        "design_rows": design_rows,
        "label_rows": label_rows,
        "action_rows": action_rows,
        "protocol_rows": protocol_rows,
        "proxy_rows": proxy_rows,
        "queue_rows": queue_rows,
        "protocol_outputs": sorted({row.get("evidence_output", "") for row in protocol_rows}),
        "cg_next_action": final.get("next_action", ""),
        "cg_claim_boundary": final.get("claim_boundary", ""),
    }


def build_polarity_plan(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    base = "label_v3_polarity_audit_pair"
    return [
        {
            "audit_id": "polarity_original_vs_flipped_split_grid",
            "source_contract": base,
            "original_diagnostic": "score original direction labels on train/validation/OOS/forward diagnostic windows",
            "flipped_diagnostic": "score sign-flipped labels side by side without selecting from forward net",
            "split_scope": "train 2022-09-01..2024-12-31; validation 2025-01-01..2025-09-30; OOS 2025-10-01..2026-04-13; forward post-2026-04-14 diagnostic only",
            "cost_ladder": "0,1,2,5,10 points for both original and flipped polarity",
            "negative_control": "direction_flip_negative_control must not become selection shortcut",
            "selection_rule": "forward data can reject but cannot choose polarity; polarity branch needs historical stability first",
            "invalid_if": "polarity chosen from post-2026-04-14 net/PF or from one curve pocket",
            "effect": "방향 뒤집기를 수익 맞춤이 아니라 사전 감사로 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "future_return_sign_map",
            "source_contract": base,
            "original_diagnostic": "map label class to realized future return sign and magnitude",
            "flipped_diagnostic": "mirror the sign map and compare class balance drift",
            "split_scope": "historical split first; forward diagnostic labeled out_of_scope_by_claim for selection",
            "cost_ladder": "same ladder by split and direction side",
            "negative_control": "label permutation should destroy sign map structure",
            "selection_rule": "accept only if sign map is stable before forward",
            "invalid_if": "using future bars beyond declared label horizon or missing bar-close boundary",
            "effect": "라벨 극성이 실제 미래수익 방향과 맞는지 눈가림 없이 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "rolling_split_polarity_stability",
            "source_contract": base,
            "original_diagnostic": "rolling calendar pockets compare original polarity hit/coverage",
            "flipped_diagnostic": "same pockets compare flipped polarity hit/coverage",
            "split_scope": "monthly or quarterly historical pockets; forward is reject-only",
            "cost_ladder": "cost2 primary with cost5/cost10 stress",
            "negative_control": "time reversal control should not preserve stability",
            "selection_rule": "no branch if only one historical pocket works",
            "invalid_if": "deleting weak hours/sessions after seeing CE runtime losses",
            "effect": "한 구간의 우연한 방향성을 전체 규칙으로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "direction_action_mapping_trace",
            "source_contract": "action_v3_transition_margin_hold12",
            "original_diagnostic": "trace model decision short/flat/long into action short/flat/long",
            "flipped_diagnostic": "trace mirrored decision into mirrored action without changing threshold",
            "split_scope": "all diagnostic splits with row-level action counts",
            "cost_ladder": "cost2 action count and expectancy before cost5 stress",
            "negative_control": "opposite-action control must be labeled diagnostic only",
            "selection_rule": "mapping can be repaired only from declared contract mismatch, not forward PnL",
            "invalid_if": "changing score threshold, lot, ATR SL/TP, or handoff while auditing mapping",
            "effect": "모델 점수가 주문 행동으로 바뀌는 지점을 따로 검산한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_label_inputs() -> list[dict[str, str]]:
    return [
        {
            "label_input_id": "label_v3_polarity_audit_pair_input",
            "label_policy_id": "label_v3_polarity_audit_pair",
            "source_fields": "timestamp/bar_close_key, close, existing label_v1 class, future_log_return_12, split id, direction side",
            "time_axis": "timestamp/bar_close_key is broker-clock alignment key; session features require event UTC mapper",
            "sample_scope": "historical train/validation/OOS plus forward diagnostic after 2026-04-14; forward cannot tune",
            "target_formula_template": "original label_v1 direction and sign-flipped diagnostic copy; no new training target selected in CH",
            "cost_buffer": "score cost0/cost1/cost2/cost5/cost10 after target construction, not fitted from forward",
            "split_policy": "time-ordered split; no random shuffle; forward is reject-only evidence",
            "forbidden_shortcut": "no polarity selection from forward net/PF/DD; no threshold tuning",
            "required_outputs": "class balance by split; sign map; polarity stability; flip control",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "label_input_id": "label_v3_lifecycle_net_cost_margin_input",
            "label_policy_id": "label_v3_lifecycle_net_cost_margin",
            "source_fields": "bar close, forward lifecycle return template, spread/slippage cost ladder, max-hold eligibility",
            "time_axis": "label horizon must use declared bar-close boundary and cannot skip to next available profitable row",
            "sample_scope": "historical splits for design; forward post-2026-04-14 diagnostic only",
            "target_formula_template": "net_lifecycle_return_after_cost_buffer with no-trade deadzone and volatility-normalized margin candidate",
            "cost_buffer": "base, +1, +2, volatility-normalized +2, +5 stress, +10 kill-switch stress",
            "split_policy": "fit buffers only on train in future run; validation/OOS/forward reject but do not tune",
            "forbidden_shortcut": "no buffer chosen after seeing forward curve pocket",
            "required_outputs": "cost ladder scorecard; lifecycle event table; worst chunk; underwater stretch; long/short attribution",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_action_inputs() -> list[dict[str, str]]:
    return [
        {
            "action_input_id": "action_v3_transition_margin_hold12_input",
            "action_policy_id": "action_v3_transition_margin_hold12",
            "required_score_inputs": "p_short, p_flat, p_long, decision label, previous decision, feature readiness flag",
            "entry_template": "enter only on declared signal transition with fixed margin and lifecycle-ready row",
            "exit_template": "max_hold_bars=12; opposite signal and flat signal are diagnostics until reviewed",
            "density_floor": "report trades/day, signal count, fill count, and sparse/fail label before any MT5 probe",
            "attribution_required": "net/PF/expectancy/DD/recovery, worst 20 trades, long/short, session/hour/month/regime",
            "risk_fixed": "lot/risk/ATR SL/TP unchanged for diagnostics",
            "forbidden_shortcut": "no session/hour/month filter from CE losses",
            "required_outputs": "action count table, transition table, density floor table, curve quality plan link",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_input_id": "action_v3_cost_margin_abstention_input",
            "action_policy_id": "action_v3_cost_margin_abstention",
            "required_score_inputs": "top direction score, runner-up score, flat score, declared cost margin",
            "entry_template": "abstain when direction score does not clear fixed predeclared cost-margin rule",
            "exit_template": "same hold12 lifecycle exit template; no profit-target tuning",
            "density_floor": "abstention cannot reduce trade count below measured floor without sparse/failed label",
            "attribution_required": "coverage, no-trade rate, cost ladder, negative controls, proxy-MT5 usability",
            "risk_fixed": "no lot optimization and no ATR mutation",
            "forbidden_shortcut": "no forward threshold search disguised as abstention",
            "required_outputs": "coverage table, no-trade table, cost ladder table, rejection reason table",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, str]]:
    return [
        {
            "control_id": "shifted_return_control",
            "control_family": "label_leakage",
            "procedure": "shift target returns away from the declared horizon and require signal quality to collapse",
            "expected_behavior": "edge disappears or is labeled invalid if preserved",
            "blocks_if": "shifted target keeps strong score or curve quality",
            "split_scope": "train/validation/OOS; forward diagnostic reject-only",
            "effect": "미래 수익을 잘못 끌어온 누수를 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "direction_flip_control",
            "control_family": "polarity",
            "procedure": "mirror direction labels and compare original/flip without using forward to choose",
            "expected_behavior": "only pre-forward stable polarity can become branch candidate later",
            "blocks_if": "flip wins only in forward or flips every pocket inconsistently",
            "split_scope": "all historical splits plus forward reject-only",
            "effect": "방향 뒤집기 자체가 또 다른 과적합이 되는 길을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "label_permutation_control",
            "control_family": "model_validation",
            "procedure": "permute labels within split and verify any future learner loses signal",
            "expected_behavior": "hit rate/proxy expectancy returns to noise-like behavior",
            "blocks_if": "permuted labels still show strong ranked edge",
            "split_scope": "train/validation/OOS only before forward use",
            "effect": "모델이 구조가 아니라 우연한 인덱스 패턴을 외우는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "time_reversal_control",
            "control_family": "time_axis",
            "procedure": "reverse time order within split diagnostics and check stability claims break",
            "expected_behavior": "temporal edge and lifecycle consistency weaken",
            "blocks_if": "reversed order preserves action edge as if time did not matter",
            "split_scope": "historical split only",
            "effect": "시간순 분할의 의미를 깨도 성과가 남는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "stale_context_carry_control",
            "control_family": "data_integrity",
            "procedure": "mark stale macro/equity context and require separate attribution before use",
            "expected_behavior": "stale context rows are separated or blocked from training authority",
            "blocks_if": "stale rows silently drive polarity/action decision",
            "split_scope": "all splits where external context is attached",
            "effect": "낡은 외부 문맥이 방향 수리를 이끄는 숨은 경로를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_forward_firewall() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_forward_polarity_selection",
            "forbidden_source": "post-2026-04-14 forward net/PF/DD/curve pocket",
            "forbidden_decision": "choose original vs flipped polarity",
            "allowed_use": "reject a historically chosen branch if it fails forward diagnostics",
            "evidence_output": rel(POLARITY_AUDIT),
            "blocks_claim": "candidate_selection;Forward Passed;Goal Achieve",
            "effect": "전진 구간을 고르는 도구가 아니라 반증 도구로만 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_forward_cost_buffer_selection",
            "forbidden_source": "forward cost ladder winners",
            "forbidden_decision": "choose label buffer, deadzone, or volatility margin",
            "allowed_use": "report fragility and reject unstable buffers",
            "evidence_output": rel(LABEL_V3_INPUT),
            "blocks_claim": "model_training_validity;candidate_selection",
            "effect": "비용 버퍼를 최신 손익에 맞춰 깎는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_forward_action_filter_selection",
            "forbidden_source": "CE bad hours/sessions/months",
            "forbidden_decision": "remove sessions, hours, months, or sides",
            "allowed_use": "slice attribution for diagnosis only",
            "evidence_output": rel(ACTION_V3_INPUT),
            "blocks_claim": "positive_judgment;Forward Passed",
            "effect": "나쁜 구간을 보고 지우는 곡선 미화 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_lot_or_threshold_rescue",
            "forbidden_source": "any diagnostic profit table",
            "forbidden_decision": "retune threshold, lot, ATR SL/TP, risk, or runtime handoff",
            "allowed_use": "stress unchanged settings and record failure",
            "evidence_output": rel(CURVE_QUALITY_PLAN),
            "blocks_claim": "runtime_authority;operating_promotion",
            "effect": "수익 개선을 로트/임계값 조정으로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "proxy_not_kpi_authority",
            "forbidden_source": "proxy-only curve or signal table",
            "forbidden_decision": "claim Forward Passed/Failed or runtime authority",
            "allowed_use": "signal sanity, feature hash parity, action count parity before MT5 probe",
            "evidence_output": rel(RUNTIME_REQUIREMENT),
            "blocks_claim": "Forward Passed;runtime_authority;live_readiness",
            "effect": "proxy(프록시)를 MT5 성과 권위로 올려치지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_runtime_requirements() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "proxy_mt5_row_parity_required",
            "required_artifact": "future MT5 telemetry and proxy expected table",
            "compare_fields": "bar_time, feature_input_hash, p_short, p_flat, p_long, decision, action",
            "acceptance_rule": "zero row mismatch on overlapping tester-visible rows before runtime claims",
            "tester_gap_rule": "if feature_last_reached_rows=0, latest pocket remains boundary-limited",
            "blocks_claim": "runtime_authority;operating_promotion",
            "effect": "Python(파이썬)과 MT5(메타트레이더5)의 의미 차이를 행 단위로 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "trade_count_and_fill_parity_required",
            "required_artifact": "MT5 order/trade telemetry and proxy action count",
            "compare_fields": "signal count, fill count, reject count, skip count, trade open/close time",
            "acceptance_rule": "action density and trade count difference must be attributed before KPI judgment",
            "tester_gap_rule": "current-day tester boundary must be named if present",
            "blocks_claim": "positive_judgment;Forward Passed",
            "effect": "신호는 맞지만 거래가 다른 상황을 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "cost_stress_runtime_required",
            "required_artifact": "spread/slippage stress table from unchanged runtime settings",
            "compare_fields": "cost0, cost1, cost2, cost5, cost10 net/PF/expectancy/DD",
            "acceptance_rule": "cost2 is primary guard; cost5/cost10 are fragility stress",
            "tester_gap_rule": "stress cannot repair missing runtime telemetry",
            "blocks_claim": "Forward Passed;Goal Achieve",
            "effect": "얇은 비용 버퍼가 다시 통과로 포장되는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "regime_attribution_runtime_required",
            "required_artifact": "session/hour/month/volatility/ADX/VIX/USD/rate slices",
            "compare_fields": "net, PF, trades/day, DD, recovery, expectancy by slice",
            "acceptance_rule": "single pocket cannot dominate positive judgment",
            "tester_gap_rule": "missing external regime rows must be labeled missing_required or blocked",
            "blocks_claim": "Forward Passed;operating_promotion",
            "effect": "한 국면의 운 좋은 곡선이 전체 강건성처럼 보이지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_curve_quality_plan() -> list[dict[str, str]]:
    return [
        {
            "metric_id": "net_pf_expectancy",
            "metric_family": "profitability",
            "required_slice": "total, long, short, session, hour, month, volatility, ADX, VIX, USD, rate",
            "minimum_evidence": "net profit, PF, expectancy, win rate, trade count, trades/day",
            "failure_signal": "PF below 1, expectancy near zero/negative, or edge concentrated in one tiny slice",
            "blocks_claim": "positive_judgment;Forward Passed",
            "effect": "수익 숫자 하나가 약한 신호를 숨기지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "metric_id": "drawdown_recovery_underwater",
            "metric_family": "risk",
            "required_slice": "total and worst pocket",
            "minimum_evidence": "max DD, recovery factor, time under water, longest underwater stretch",
            "failure_signal": "curve stays underwater or recovery depends on one late burst",
            "blocks_claim": "Forward Passed;Goal Achieve",
            "effect": "예쁜 수익곡선 요구를 DD와 회복력으로 검산한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "metric_id": "worst_chunk_curve_pocket",
            "metric_family": "curve_shape",
            "required_slice": "rolling 20 trades, rolling day/week/month chunks",
            "minimum_evidence": "worst chunk net, PF, consecutive loss, pocket attribution",
            "failure_signal": "one pocket destroys a large share of gains or repeated local collapses",
            "blocks_claim": "Forward Passed",
            "effect": "전체 수익이 좋아도 깨지는 곡선 포켓을 따로 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "metric_id": "density_and_side_balance",
            "metric_family": "trade_shape",
            "required_slice": "long/short and model family branch",
            "minimum_evidence": "trades/day, side mix, skip/reject/fill counts, sparse branch label",
            "failure_signal": "too few trades, one-side collapse, or sparse branch PF illusion",
            "blocks_claim": "candidate_selection;Forward Passed",
            "effect": "거래수가 없는 예쁜 곡선을 통과로 오해하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "metric_id": "lot_normalized_cost_stress",
            "metric_family": "execution_cost",
            "required_slice": "base lot and normalized one-lot diagnostics",
            "minimum_evidence": "lot-normalized net, spread/slippage stress, unchanged lot policy note",
            "failure_signal": "profit disappears after lot normalization or cost2 stress",
            "blocks_claim": "Forward Passed;runtime_authority",
            "effect": "로트 크기나 비용 가정이 알파처럼 보이는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "metric_id": "proxy_vs_mt5_usability",
            "metric_family": "runtime_parity",
            "required_slice": "overlapping tester-visible rows and tester gap boundary",
            "minimum_evidence": "proxy expected vs MT5 row parity, mismatch count, feature_last_reached",
            "failure_signal": "proxy and MT5 diverge or latest tester gap is ignored",
            "blocks_claim": "Forward Passed;runtime_authority",
            "effect": "proxy 테스트를 실제 MT5 사용 가능성 판단과 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_next_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CI_review_materialized_label_action_inputs",
            "next_run_id": NEXT_RUN_ID,
            "task": "review CH polarity, label, action, negative-control, firewall, runtime, and curve-quality inputs before any training",
            "required_inputs": ";".join(rel(path) for path in (POLARITY_AUDIT, LABEL_V3_INPUT, ACTION_V3_INPUT, NEGATIVE_CONTROL, FORWARD_FIREWALL, RUNTIME_REQUIREMENT, CURVE_QUALITY_PLAN)),
            "required_outputs": "input_review_matrix.csv;no_overfit_gate_review.csv;run337CJ_training_or_block_queue.csv",
            "blocked_if_missing": "any firewall, negative control, or runtime requirement is missing or inconsistent",
            "forbidden_shortcut": "do not train, tune threshold, optimize lot, select candidate, or claim Forward Passed in CI",
            "effect": "CH 입력을 검토해서 학습으로 넘길 수 있는지 또는 차단해야 하는지 판단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(summary: Mapping[str, Any]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "bar_close_key/timestamp is broker-clock alignment key; timestamp_event_utc must be mapped before session features",
        "sample_scope": "US100 M5 historical split through 2026-04-13 plus post-2026-04-14 forward diagnostics as reject-only evidence",
        "missing_or_duplicate_check": "not_applicable_design_inputs; downstream run must check row-level gaps before training",
        "feature_label_boundary": "features remain fixed inputs; labels/actions are contracts only; future bars cannot enter feature rows",
        "split_boundary": "time-ordered train/validation/OOS; forward cannot tune polarity, threshold, model, lot, or action",
        "leakage_risk": "forward polarity/action selection and stale external context carry",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "not_trained_in_run337CH",
        "target_and_label": "label_v3 polarity/lifecycle cost-margin input contracts only",
        "split_method": "time-ordered historical split with forward reject-only diagnostics",
        "selection_metric": "not_applicable_no_selection",
        "secondary_metrics": "cost ladder, density floor, curve pocket, proxy-MT5 parity requirement",
        "threshold_policy": "no threshold tuning",
        "overfit_risk": "using forward losses to pick polarity/action/cost buffer",
        "calibration_risk": "future scores must not be treated as probabilities without calibration evidence",
        "comparison_baseline": "CG failure attribution and CE runtime probe",
        "validation_judgment": "exploratory_input_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in (POLARITY_AUDIT, LABEL_V3_INPUT, ACTION_V3_INPUT, NEGATIVE_CONTROL, FORWARD_FIREWALL, RUNTIME_REQUIREMENT, CURVE_QUALITY_PLAN, NEXT_QUEUE, REPORT_PATH)],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "materialized input contracts, no-overfit firewall, negative controls, runtime requirements, gate audit",
        "evidence_missing": "no model training, no MT5 runtime probe, no forward decision",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": "CI must review input consistency before any CJ training/materialization queue",
        "user_explanation_hook": "입력은 준비됐지만 아직 새 ONNX나 전진 통과 주장은 아니다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    hashes = {rel(path): sha256_file(path) for path in paths if path_exists(path) and path != LINEAGE_RECEIPT}
    lineage_receipt["artifact_hashes"] = hashes
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def build_gates(summary: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, str]]:
    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    protocol_outputs = set(summary["protocol_outputs"])
    required_firewalls = {
        "no_forward_polarity_selection",
        "no_forward_cost_buffer_selection",
        "no_forward_action_filter_selection",
        "no_lot_or_threshold_rescue",
        "proxy_not_kpi_authority",
    }
    observed_firewalls = {item.get("firewall_id", "") for item in outputs["firewall"]}
    return [
        row("ch_gate_inputs_present", not summary["missing_inputs"], ";".join(summary["missing_inputs"]) or "none", "no_missing_inputs", "CG 설계 산출물과 대기열을 실제 입력으로 연결한다."),
        row("ch_gate_parent_points_to_ch", summary["cg_next_action"] == RUN_ID, summary["cg_next_action"], RUN_ID, "현재 실행이 이전 실행의 next_action(다음 행동)과 맞는다."),
        row("ch_gate_required_outputs_materialized", all(len(outputs[key]) > 0 for key in ("polarity", "label", "action", "negative", "firewall", "runtime", "curve", "queue")), {key: len(value) for key, value in outputs.items()}, "all_output_row_counts_positive", "검토 가능한 입력 계약을 빈 파일로 남기지 않는다."),
        row("ch_gate_forward_firewall", required_firewalls.issubset(observed_firewalls), ";".join(sorted(observed_firewalls)), "all required firewall IDs", "전진 구간을 선택 도구로 쓰지 못하게 한다."),
        row("ch_gate_negative_controls", len(outputs["negative"]) >= 5, len(outputs["negative"]), ">=5 negative controls", "방향/라벨/시간축/문맥 누수 대조군을 학습 전 요구한다."),
        row("ch_gate_runtime_requirement", len(outputs["runtime"]) >= 4, len(outputs["runtime"]), ">=4 runtime requirements", "proxy-MT5(프록시-MT5) 사용성 판단을 다음 런타임 요구사항으로 묶는다."),
        row("ch_gate_curve_quality_plan", len(outputs["curve"]) >= 6, len(outputs["curve"]), ">=6 curve quality rows", "예쁜 수익곡선 요구를 정량 검토 항목으로 고정한다."),
        row("ch_gate_no_training_or_selection", True, "model_training=not_run;candidate_selection=not_run", "no_training_no_selection", "CH를 입력 물질화로만 제한한다."),
        row("ch_gate_protocol_coverage", {"forward_selection_firewall.csv", "negative_control_plan.csv", "runtime_probe_requirement.csv", "curve_quality_measurement_plan.csv"}.issubset(protocol_outputs), ";".join(sorted(protocol_outputs)), "CG protocol outputs covered", "CG의 필수 게이트를 실제 파일로 대응시킨다."),
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CH Directional Label/Action Repair Inputs(방향 라벨/행동 수리 입력)

## Conclusion(결론)

run337CH(337CH 실행)는 run337CG(337CG 실행)의 설계를 실제 입력 계약으로 물질화했다.

Effect(효과): polarity audit(극성 감사), label v3(라벨 v3), action v3(행동 v3), negative controls(부정 대조), forward selection firewall(전진 선택 방화벽), runtime requirement(런타임 요구사항), curve quality plan(곡선 품질 계획)을 다음 review(검토)에서 검사할 수 있다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- polarity_plan_rows(극성 계획 행): `{final["polarity_plan_rows"]}`
- label_input_rows(라벨 입력 행): `{final["label_input_rows"]}`
- action_input_rows(행동 입력 행): `{final["action_input_rows"]}`
- negative_control_rows(부정 대조 행): `{final["negative_control_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- runtime_requirement_rows(런타임 요구 행): `{final["runtime_requirement_rows"]}`
- curve_quality_rows(곡선 품질 행): `{final["curve_quality_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Outputs(산출물)

- polarity_audit_plan(극성 감사 계획): `{rel(POLARITY_AUDIT)}`
- label_v3_input_contract(라벨 v3 입력 계약): `{rel(LABEL_V3_INPUT)}`
- action_v3_input_contract(행동 v3 입력 계약): `{rel(ACTION_V3_INPUT)}`
- negative_control_plan(부정 대조 계획): `{rel(NEGATIVE_CONTROL)}`
- forward_selection_firewall(전진 선택 방화벽): `{rel(FORWARD_FIREWALL)}`
- runtime_probe_requirement(런타임 탐침 요구): `{rel(RUNTIME_REQUIREMENT)}`
- curve_quality_measurement_plan(곡선 품질 측정 계획): `{rel(CURVE_QUALITY_PLAN)}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CH

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 방향/라벨/행동 수리 설계를 학습 전 검토 가능한 입력 계약으로 물질화했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FINAL_DECISION)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {NEXT_RUN_ID}", 1)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CH focus complete: directional label/action repair inputs(방향 라벨/행동 수리 입력)을 `{STATUS}`로 물질화했다. "
        "Effect(효과): polarity/label/action/negative-control/runtime/curve gates(극성/라벨/행동/부정대조/런타임/곡선 게이트)를 run337CI(337CI 실행)에서 검토한다."
    )
    if "Stage337 run337CH focus complete" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337CH(337CH 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): polarity audit(극성 감사), label/action input contract(라벨/행동 입력 계약), negative controls(부정 대조), runtime requirement(런타임 요구), curve quality plan(곡선 품질 계획)을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CH(337CH 실행)" not in current_text:
        marker = "## Stage337 run337CG(337CG"
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_ch_input_materialization_only_run337CE_reviewed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 materialized repair inputs(물질화된 수리 입력) 검토다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CH(337CH 실행) materialized directional label/action repair inputs(방향 라벨/행동 수리 입력). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CH materialized directional label/action policy repair inputs(방향 라벨/행동 정책 수리 입력) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "directional_label_action_policy_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "directional_label_action_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_input_materialization",
        "tier_scope": "out_of_scope_by_claim_input_contract_no_tier_kpi",
        "kpi_scope": "input_contract_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": "not_applicable_input_contract_only",
        "guardrail_kpi": "no_forward_selection;negative_controls;runtime_requirement;curve_quality_plan",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CG design contracts materialized",
        "kpi_scope": "input_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__directional_label_action_inputs",
        "family": "data_integrity_model_validation_artifact_lineage",
        "question": "are label/action repair inputs materialized before training without forward selection",
        "metric_scope": "input_contract_no_forward_decision",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]

    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    summary = summarize_inputs()
    polarity_rows = build_polarity_plan(summary)
    label_rows = build_label_inputs()
    action_rows = build_action_inputs()
    negative_rows = build_negative_controls()
    firewall_rows = build_forward_firewall()
    runtime_rows = build_runtime_requirements()
    curve_rows = build_curve_quality_plan()
    queue_rows = build_next_queue()
    outputs = {
        "polarity": polarity_rows,
        "label": label_rows,
        "action": action_rows,
        "negative": negative_rows,
        "firewall": firewall_rows,
        "runtime": runtime_rows,
        "curve": curve_rows,
        "queue": queue_rows,
    }
    gates = build_gates(summary, outputs)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "polarity_plan_rows": len(polarity_rows),
        "label_input_rows": len(label_rows),
        "action_input_rows": len(action_rows),
        "negative_control_rows": len(negative_rows),
        "firewall_rows": len(firewall_rows),
        "runtime_requirement_rows": len(runtime_rows),
        "curve_quality_rows": len(curve_rows),
        "queue_rows": len(queue_rows),
        "data_integrity_judgment": "usable_with_boundary",
        "lineage_judgment": "connected_with_boundary",
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(POLARITY_AUDIT, POLARITY_COLUMNS, polarity_rows),
        write_csv(LABEL_V3_INPUT, LABEL_INPUT_COLUMNS, label_rows),
        write_csv(ACTION_V3_INPUT, ACTION_INPUT_COLUMNS, action_rows),
        write_csv(NEGATIVE_CONTROL, NEGATIVE_COLUMNS, negative_rows),
        write_csv(FORWARD_FIREWALL, FIREWALL_COLUMNS, firewall_rows),
        write_csv(RUNTIME_REQUIREMENT, RUNTIME_COLUMNS, runtime_rows),
        write_csv(CURVE_QUALITY_PLAN, CURVE_COLUMNS, curve_rows),
        write_csv(NEXT_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(summary))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
