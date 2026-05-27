from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CG"
RUN_ID = "run337CG_design_directional_label_action_policy_repair_without_db_v1"
PARENT_RUN_ID = "run337CF_review_lifecycle_aware_runtime_probe_and_failure_attribution_without_db_v1"
NEXT_RUN_ID = "run337CH_materialize_directional_label_action_policy_repair_inputs_without_db_v1"
STATUS = "completed_stage337CG_directional_label_action_policy_repair_design_no_training_no_selection"
JUDGMENT = "direction_cost_failure_converted_to_predeclared_no_overfit_repair_design"
DECISION = "stage337CG_open_run337CH_materialize_directional_label_action_policy_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CG_directional_label_action_policy_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CG_directional_label_action_policy_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CG_directional_label_action_policy_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CF_DIR = STAGE_DIR / "02_runs" / "run337CF"
CF_FINAL = CF_DIR / "final_decision.json"
CF_RUNTIME = CF_DIR / "runtime_parity_attribution.csv"
CF_COST = CF_DIR / "cost_direction_failure_attribution.csv"
CF_SIGNAL = CF_DIR / "signal_quality_attribution.csv"
CF_QUEUE = CF_DIR / "run337CG_directional_label_action_policy_repair_queue.csv"

DESIGN_MATRIX = RUN_DIR / "directional_label_action_repair_design_matrix.csv"
LABEL_CONTRACT = RUN_DIR / "label_policy_repair_contract.csv"
ACTION_CONTRACT = RUN_DIR / "action_policy_repair_contract.csv"
VALIDATION_PROTOCOL = RUN_DIR / "no_overfit_validation_protocol.csv"
PROXY_MT5_POLICY = RUN_DIR / "proxy_mt5_usability_policy.csv"
NEXT_QUEUE = RUN_DIR / "run337CH_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (CF_FINAL, CF_RUNTIME, CF_COST, CF_SIGNAL, CF_QUEUE)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    LABEL_CONTRACT,
    ACTION_CONTRACT,
    VALIDATION_PROTOCOL,
    PROXY_MT5_POLICY,
    NEXT_QUEUE,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_RECEIPT,
    REQUIRED_GATE_AUDIT,
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

DESIGN_COLUMNS = (
    "design_id",
    "repair_family",
    "hypothesis",
    "changed_variable",
    "fixed_variables",
    "source_evidence",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "next_materialization",
    "claim_boundary",
)
LABEL_COLUMNS = (
    "label_policy_id",
    "label_family",
    "target_definition",
    "polarity_policy",
    "cost_buffer_policy",
    "split_policy",
    "forbidden_shortcut",
    "required_diagnostics",
    "claim_boundary",
)
ACTION_COLUMNS = (
    "action_policy_id",
    "entry_rule",
    "exit_rule",
    "direction_policy",
    "density_policy",
    "risk_policy",
    "forbidden_shortcut",
    "required_diagnostics",
    "claim_boundary",
)
VALIDATION_COLUMNS = (
    "gate_id",
    "gate_family",
    "required_check",
    "evidence_output",
    "blocks_claim",
    "effect",
    "claim_boundary",
)
PROXY_POLICY_COLUMNS = (
    "policy_id",
    "usable_for",
    "not_usable_for",
    "required_compare",
    "tester_gap_rule",
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


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except (ValueError, RuntimeError):
        return item.as_posix()


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
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_bytes(text.encode(encoding))
    return path


def replace_bullet_value(text: str, field_name: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"- {field_name}(") or line.startswith(f"- {field_name}:"):
            prefix = line.split(":", 1)[0]
            lines[index] = f"{prefix}: {value}"
            break
    trailing = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + trailing


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def upsert_csv(path: Path, key_column: str, row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    rows = [item for item in rows if str(item.get(key_column, "")) != str(row.get(key_column, ""))]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def summarize_inputs() -> dict[str, Any]:
    parent = read_json(CF_FINAL)
    runtime = read_csv(CF_RUNTIME)
    cost = read_csv(CF_COST)
    signal = read_csv(CF_SIGNAL)
    runtime_mismatches = sum(int(row.get("mismatch_rows") or 0) for row in runtime)
    direction_failed = sum(1 for row in cost if row.get("direction_control_status") == "failed")
    cost2_failed = sum(1 for row in cost if str(row.get("cost2_guard_status", "")).endswith("failed_guard"))
    weak_signal = sum(1 for row in signal if row.get("signal_quality_status") == "weak_signal_quality_below_random_like_threshold")
    logreg_trades = [float(row.get("mt5_trade_count") or 0) for row in cost if row.get("model_family") == "logreg"]
    tree_trades = [float(row.get("mt5_trade_count") or 0) for row in cost if row.get("model_family") == "extratrees"]
    return {
        "parent": parent,
        "runtime": runtime,
        "cost": cost,
        "signal": signal,
        "runtime_mismatches": runtime_mismatches,
        "direction_failed": direction_failed,
        "cost2_failed": cost2_failed,
        "weak_signal": weak_signal,
        "model_rows": len(cost),
        "signal_rows": len(signal),
        "avg_logreg_trades": sum(logreg_trades) / len(logreg_trades) if logreg_trades else 0.0,
        "avg_tree_trades": sum(tree_trades) / len(tree_trades) if tree_trades else 0.0,
    }


def build_design_matrix(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "design_id": "polarity_audit_before_any_flip",
            "repair_family": "direction_label_polarity",
            "hypothesis": "direction control(방향 대조) 6/6 실패는 라벨 극성(label polarity, 라벨 극성) 또는 action mapping(행동 매핑) 오류 가능성을 먼저 감사해야 한다.",
            "changed_variable": "none yet; CH only materializes polarity audit tables and paired original/flip diagnostic plans",
            "fixed_variables": "feature order, raw data, split boundaries, threshold identities, lot/risk, MT5 handoff",
            "source_evidence": rel(CF_COST),
            "success_criteria": "original and flipped polarity are compared on train/validation/oos/forward diagnostics without selecting from forward data",
            "failure_criteria": "flip looks good only in forward or negative controls still fail after polarity audit",
            "invalid_conditions": "using forward PnL to choose polarity, changing threshold, deleting bad hours after seeing results",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "cost_buffer_label_v3_contract",
            "repair_family": "cost_aware_label",
            "hypothesis": "cost2 guard(비용2 가드) 6/6 실패는 label target(라벨 목표)이 거래 비용과 실제 lifecycle(생애주기)을 충분히 반영하지 못했음을 뜻한다.",
            "changed_variable": "future training label candidates only: lifecycle net return, cost ladder, no-trade deadzone, volatility-normalized margin",
            "fixed_variables": "no forward threshold tuning, no lot optimization, no candidate selection in design/materialization",
            "source_evidence": rel(CF_COST),
            "success_criteria": "future labels must declare cost0/1/2/5/10 scorecards before any model is trained",
            "failure_criteria": "positive base result collapses at +1 or +2 cost, or trade density becomes unusably sparse",
            "invalid_conditions": "building the label from forward runtime losses, or fitting label buffers on post-2026-04-14 data",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "action_transition_lifecycle_policy",
            "repair_family": "action_policy",
            "hypothesis": "same model scores may be less harmful if action policy(행동 정책) requires transition, cost margin, and max-hold lifecycle consistency before entry.",
            "changed_variable": "entry transition, flat handling, opposite-signal reversal, max-hold action diagnostics",
            "fixed_variables": "score threshold values are not optimized on forward, ATR/risk/lot remain unchanged for diagnostics",
            "source_evidence": rel(CF_RUNTIME),
            "success_criteria": "future materialization reports trade count, long/short mix, fill rate, expectancy, DD, and lifecycle proxy for every action variant",
            "failure_criteria": "trade density collapses or action policy merely hides losing pockets post-hoc",
            "invalid_conditions": "filtering sessions/hours/months after looking at CE MT5 net profit",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "sparse_tree_keepout_and_linear_density_control",
            "repair_family": "model_family_guard",
            "hypothesis": "ExtraTrees(엑스트라트리) variants are too sparse while logreg(로지스틱 회귀) variants have usable density but weak edge.",
            "changed_variable": "future model family queue priority and density floor diagnostics only",
            "fixed_variables": "no model selected; no branch promoted; no threshold search",
            "source_evidence": rel(CF_COST),
            "success_criteria": "future training must report density floor, effective trades/day, and worst 20-trade pocket before ONNX packaging",
            "failure_criteria": "sparse nonlinear branch has low PF and low trade count again, or dense linear branch remains PF below 1",
            "invalid_conditions": "selecting model family from forward-only net profit",
            "next_materialization": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_label_contract() -> list[dict[str, Any]]:
    return [
        {
            "label_policy_id": "label_v3_polarity_audit_pair",
            "label_family": "direction_polarity_control",
            "target_definition": "materialize original and sign-flipped target diagnostics side by side; do not train or select in CH",
            "polarity_policy": "polarity can become a predeclared branch only after historical train/validation/oos audit, never from forward net alone",
            "cost_buffer_policy": "same cost ladder is scored for both polarities: 0,1,2,5,10 points",
            "split_policy": "train/validation/oos from historical model input; post-2026-04-14 remains diagnostic only",
            "forbidden_shortcut": "no forward data polarity selection; no threshold retuning; no lot optimization",
            "required_diagnostics": "class balance, future return sign map, direction flip negative control, rolling split polarity stability",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "label_policy_id": "label_v3_lifecycle_net_cost_margin",
            "label_family": "lifecycle_cost_margin",
            "target_definition": "future label candidate must be based on lifecycle net return after predeclared cost buffer and no-trade deadzone",
            "polarity_policy": "uses audited polarity from label_v3_polarity_audit_pair; unknown polarity stays blocked",
            "cost_buffer_policy": "minimum train-time candidate buffers: base threshold, +1, +2, volatility-normalized +2, and +5 stress",
            "split_policy": "fit only on train; validation/oos/forward can reject but not tune thresholds",
            "forbidden_shortcut": "no changing buffers after seeing forward curve pocket",
            "required_diagnostics": "cost ladder scorecard, lifecycle event table, worst chunk, underwater stretch, long/short attribution",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_action_contract() -> list[dict[str, Any]]:
    return [
        {
            "action_policy_id": "action_v3_transition_margin_hold12",
            "entry_rule": "enter only on predeclared signal transition with fixed probability margin and lifecycle-ready row",
            "exit_rule": "max_hold_bars 12, opposite signal diagnostic, flat signal diagnostic; no profit-target tuning in CH",
            "direction_policy": "long and short must be reported separately; one-side keepout requires predeclared validation before use",
            "density_policy": "minimum density floor must be measured before MT5 probe package: trades/day and branch signal count",
            "risk_policy": "lot/risk unchanged for diagnostics; no lot optimization",
            "forbidden_shortcut": "no session/hour/month filter from CE losses",
            "required_diagnostics": "trade count, fill count, net/PF/expectancy/DD/recovery, worst 20 trades, long/short, session/hour/month",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_policy_id": "action_v3_cost_margin_abstention",
            "entry_rule": "abstain when top direction score does not clear fixed cost-margin confidence rule declared before training",
            "exit_rule": "same as action_v3_transition_margin_hold12",
            "direction_policy": "polarity audit must pass before direction score is treated as executable",
            "density_policy": "abstention cannot reduce trade count below materialized density floor without being labeled sparse/failed",
            "risk_policy": "no ATR SL/TP change in design; later stress may compare unchanged runtime settings only",
            "forbidden_shortcut": "no forward threshold search disguised as abstention",
            "required_diagnostics": "coverage, no-trade rate, cost ladder, negative controls, proxy-MT5 usability",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_validation_protocol() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "cg_gate_no_forward_selection",
            "gate_family": "overfit_firewall",
            "required_check": "CH may materialize forward diagnostics, but cannot select polarity, threshold, model, lot, or action policy from forward net.",
            "evidence_output": "forward_selection_firewall.csv",
            "blocks_claim": "candidate_selection;Forward Passed;Goal Achieve",
            "effect": "forward data(전진 데이터)를 수리 재료가 아니라 반증 자료로만 쓰게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cg_gate_negative_controls",
            "gate_family": "model_validation",
            "required_check": "shifted return, direction flip, label permutation, and time-reversal controls must be scored before training claims.",
            "evidence_output": "negative_control_plan.csv",
            "blocks_claim": "model_training_validity;candidate_selection",
            "effect": "우연한 방향 뒤집기나 데이터 누수를 빠르게 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cg_gate_runtime_parity_required",
            "gate_family": "runtime_parity",
            "required_check": "Any future ONNX must repeat proxy-MT5 row comparison like CE before runtime claims.",
            "evidence_output": "runtime_probe_requirement.csv",
            "blocks_claim": "runtime_authority;operating_promotion",
            "effect": "Python(파이썬) 성공을 MT5 성공으로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cg_gate_curve_quality_required",
            "gate_family": "performance_attribution",
            "required_check": "Net/PF must be paired with DD, recovery, worst chunk, underwater stretch, long/short, session/hour/month/regime slices.",
            "evidence_output": "curve_quality_measurement_plan.csv",
            "blocks_claim": "positive_judgment;Forward Passed",
            "effect": "예쁜 수익곡선 요구를 단일 net profit(순수익)으로 축소하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_policy() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "proxy_mt5_overlap_usable_for_signal_parity",
            "usable_for": "feature hash, probability output, decision label, action count parity on overlapping tester-visible rows",
            "not_usable_for": "Forward Passed/Failed, runtime authority, live readiness, operating promotion",
            "required_compare": "bar_time, feature_input_hash, p_short/p_flat/p_long, decision/action, signal count, trade count",
            "tester_gap_rule": "if feature_last_reached_rows is 0, latest pocket remains boundary-limited",
            "effect": "CE에서 확인된 proxy-MT5 일치를 다음 수리의 런타임 계약으로 재사용한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CH_materialize_polarity_label_action_inputs",
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize polarity audit, label v3 contract inputs, action v3 contract inputs, validation protocol, and proxy-MT5 usability templates",
            "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(LABEL_CONTRACT)};{rel(ACTION_CONTRACT)};{rel(VALIDATION_PROTOCOL)}",
            "required_outputs": "polarity_audit_plan.csv;label_v3_input_contract.csv;action_v3_input_contract.csv;negative_control_plan.csv;runtime_probe_requirement.csv",
            "blocked_if_missing": "any no-forward-selection firewall or negative control plan is missing",
            "forbidden_shortcut": "do not train a new model in CH; do not tune threshold; do not select candidate",
            "effect": "CG 설계를 다음 실행에서 실제 입력 계약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(summary: Mapping[str, Any], rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    parent = summary["parent"]
    return [
        row("cg_gate_parent_cf_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "CF가 CG 설계를 열었는지 확인한다."),
        row("cg_gate_runtime_mismatch_zero", summary["runtime_mismatches"] == 0, f"runtime_mismatches={summary['runtime_mismatches']}", "0", "런타임 문제가 아니라 신호/행동 문제로 설계 경계를 고정한다."),
        row("cg_gate_direction_failure_all_named", summary["direction_failed"] == summary["model_rows"], f"direction_failed={summary['direction_failed']}/{summary['model_rows']}", "all models", "방향 대조 실패를 설계 핵심 원인으로 둔다."),
        row("cg_gate_cost2_failure_all_named", summary["cost2_failed"] == summary["model_rows"], f"cost2_failed={summary['cost2_failed']}/{summary['model_rows']}", "all models", "비용2 실패를 설계 핵심 원인으로 둔다."),
        row("cg_gate_design_rows", len(rows["design"]) >= 4, f"design_rows={len(rows['design'])}", ">=4", "방어/공격/수리 균형 설계가 실제 행으로 있다."),
        row("cg_gate_label_action_contracts", len(rows["label"]) >= 2 and len(rows["action"]) >= 2, f"label={len(rows['label'])};action={len(rows['action'])}", "label>=2;action>=2", "라벨과 행동 정책을 따로 검증 가능하게 한다."),
        row("cg_gate_validation_protocol", len(rows["validation"]) >= 4, f"validation_rows={len(rows['validation'])}", ">=4", "과적합/동등성/곡선 품질 게이트를 다음 실행으로 넘긴다."),
        row("cg_gate_next_queue", len(rows["queue"]) == 1, f"queue_rows={len(rows['queue'])}", "1", "다음 CH 물질화 실행을 연다."),
        row("cg_gate_no_forward_or_goal_claim", True, "Forward/Goal not_claimed", "no forbidden claim", "설계를 운영 주장으로 키우지 않는다."),
    ]


def build_receipts(summary: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "hypothesis": "Direction/cost failure can be converted into predeclared polarity, label, and action repair inputs without forward overfitting.",
                "decision_use": "opens CH materialization only; no model training or selection",
                "comparison_baseline": rel(CF_COST),
                "control_variables": "feature order, historical split, fixed thresholds, lot/risk, proxy-MT5 comparison contract",
                "changed_variables": "future label/action policy candidates are designed, not trained",
                "sample_scope": "Stage337 CF evidence; no new sample created",
                "success_criteria": "materialized design and gates that prevent forward threshold tuning",
                "failure_criteria": "missing polarity audit, missing negative controls, or forward selection leakage",
                "invalid_conditions": "using forward PnL to select polarity/action",
                "stop_conditions": "do not train until CH materializes audit inputs",
                "evidence_plan": [rel(DESIGN_MATRIX), rel(LABEL_CONTRACT), rel(ACTION_CONTRACT), rel(VALIDATION_PROTOCOL), rel(NEXT_QUEUE)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "run_id": RUN_ID,
                "model_family": "future models only; no model trained in CG",
                "target_and_label": "label v3 candidates designed but not materialized as training data",
                "split_method": "historical train/validation/oos plus forward diagnostic boundary inherited from Stage337",
                "selection_metric": "none",
                "secondary_metrics": "cost ladder, long/short, curve pocket, density, negative controls, proxy-MT5 parity",
                "threshold_policy": "fixed or predeclared only; no forward threshold tuning",
                "overfit_risk": "using CE losses to choose polarity/action after the fact",
                "calibration_risk": "scores remain rank/decision scores until calibrated",
                "comparison_baseline": rel(CF_COST),
                "validation_judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "future CH/CI package; no MT5 run in CG",
                "shared_contract": "proxy-MT5 comparison remains required before runtime claims",
                "known_differences": "tester feature_last gap remains from CE",
                "parity_check": rel(PROXY_MT5_POLICY),
                "runtime_claim_boundary": "research_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "run_id": RUN_ID,
                "observed_change": "runtime parity cleared but direction and cost failed for all CD models",
                "comparison_baseline": rel(CF_COST),
                "likely_drivers": "label polarity/action mapping, cost buffer, weak OOS signal quality, sparse nonlinear trade shape",
                "segment_checks": "deferred to CH materialization plan",
                "trade_shape": f"avg_logreg_trades={summary['avg_logreg_trades']};avg_tree_trades={summary['avg_tree_trades']}",
                "alternative_explanations": "tester gap still blocks latest-pocket forward decision",
                "attribution_confidence": "medium",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(DESIGN_MATRIX), rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "materialized inputs, training, ONNX, MT5 runtime probe, Forward Passed/Failed",
                "judgment_label": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "런타임은 맞았으니 이제 방향/비용/행동 설계를 과적합 없이 다시 세운다.",
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "run_id": RUN_ID,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_report(summary: Mapping[str, Any]) -> Path:
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CG Directional Label/Action Repair Design(방향 라벨/행동 수리 설계)

## Conclusion(결론)

run337CG(337CG 실행)는 CF의 실패를 새 모델 학습으로 바로 넘기지 않고, polarity audit(극성 감사), label v3(라벨 v3), action v3(행동 v3), no-overfit validation(무과적합 검증)을 먼저 설계했다.

Effect(효과): 방향을 뒤집어 좋아 보이는 위험을 forward overfit(전진 과적합)로 만들지 않고, 다음 CH에서 검증 가능한 입력 계약으로 바꾼다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- runtime_mismatches(런타임 불일치): `{summary['runtime_mismatches']}`
- direction_failed_models(방향 실패 모델): `{summary['direction_failed']}/{summary['model_rows']}`
- cost2_failed_models(비용2 실패 모델): `{summary['cost2_failed']}/{summary['model_rows']}`
- weak_signal_rows(약한 신호 행): `{summary['weak_signal']}/{summary['signal_rows']}`

## Outputs(산출물)

- design_matrix(설계 행렬): `{rel(DESIGN_MATRIX)}`
- label_contract(라벨 계약): `{rel(LABEL_CONTRACT)}`
- action_contract(행동 계약): `{rel(ACTION_CONTRACT)}`
- validation_protocol(검증 프로토콜): `{rel(VALIDATION_PROTOCOL)}`
- proxy_policy(프록시 정책): `{rel(PROXY_MT5_POLICY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc() -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CG Directional Label/Action Repair Design(결정: 방향 라벨/행동 수리 설계)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): 다음 run337CH(337CH 실행)는 학습이 아니라 polarity audit(극성 감사), label/action contract(라벨/행동 계약), negative control(부정 대조), proxy-MT5 usability(프록시-MT5 사용성) 입력을 물질화한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {NEXT_RUN_ID}", 1)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CG focus complete: directional label/action policy repair design(방향 라벨/행동 정책 수리 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): polarity/label/action/no-overfit inputs(극성/라벨/행동/무과적합 입력)을 run337CH(337CH 실행)로 물질화한다.\n"
    )
    if "Stage337 run337CG focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current = current_text
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_value(current, field_name, value)
    section = f"""
## Stage337 run337CG(337CG 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 방향/비용 실패를 polarity audit(극성 감사), label v3(라벨 v3), action v3(행동 v3), no-overfit validation(무과적합 검증) 계약으로 바꿨다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CG(337CG 실행)" not in current:
        marker = "## Stage337 run337CF(337CF"
        current = current.replace(marker, section + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_cg_design_only_run337CE_reviewed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 directional label/action policy repair inputs(방향 라벨/행동 정책 수리 입력) 물질화다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CG(337CG 실행) designed directional label/action policy repair(방향 라벨/행동 정책 수리). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CG designed directional label/action policy repair(방향 라벨/행동 정책 수리) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "directional_label_action_policy_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "directional_label_action_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_design",
        "tier_scope": "out_of_scope_by_claim_design_no_tier_kpi",
        "kpi_scope": "design_contract_no_training",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": "not_applicable_design_only",
        "guardrail_kpi": "no_forward_selection;negative_controls_required;proxy_mt5_required",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation",
        "evidence_scope": "CF runtime/cost/direction/signal attribution",
        "kpi_scope": "design_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__directional_label_action_design",
        "family": "experiment_design_model_validation",
        "question": "how to repair direction label and action policy without forward overfitting",
        "metric_scope": "design_only_no_forward_decision",
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
    design_rows = build_design_matrix(summary)
    label_rows = build_label_contract()
    action_rows = build_action_contract()
    validation_rows = build_validation_protocol()
    proxy_rows = build_proxy_policy()
    queue_rows = build_next_queue()
    rows = {
        "design": design_rows,
        "label": label_rows,
        "action": action_rows,
        "validation": validation_rows,
        "proxy": proxy_rows,
        "queue": queue_rows,
    }
    gates = build_gates(summary, rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "design_rows": len(design_rows),
        "label_contract_rows": len(label_rows),
        "action_contract_rows": len(action_rows),
        "validation_protocol_rows": len(validation_rows),
        "proxy_policy_rows": len(proxy_rows),
        "queue_rows": len(queue_rows),
        "runtime_mismatches": summary["runtime_mismatches"],
        "direction_failed_models": summary["direction_failed"],
        "cost2_failed_models": summary["cost2_failed"],
        "weak_signal_rows": summary["weak_signal"],
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
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design_rows),
        write_csv(LABEL_CONTRACT, LABEL_COLUMNS, label_rows),
        write_csv(ACTION_CONTRACT, ACTION_COLUMNS, action_rows),
        write_csv(VALIDATION_PROTOCOL, VALIDATION_COLUMNS, validation_rows),
        write_csv(PROXY_MT5_POLICY, PROXY_POLICY_COLUMNS, proxy_rows),
        write_csv(NEXT_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(summary))
    artifacts.append(write_report(summary))
    artifacts.append(write_decision_doc())
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
