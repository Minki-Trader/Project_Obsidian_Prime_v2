from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337X"
RUN_ID = "run337X_review_materialized_cost_buffer_source_policy_repair_inputs_v1"
PARENT_RUN_ID = "run337W_materialize_cost_buffer_source_policy_repair_inputs_v1"
NEXT_RUN_ID = "run337Y_materialize_actual_source_age_proxy_mt5_repair_probe_inputs_v1"
STATUS = "completed_stage337X_materialized_inputs_review_evidence_gaps_bound_no_training_no_mt5"
JUDGMENT = "input_contracts_complete_but_evidence_maturity_blocks_training_forward_runtime_claims"
DECISION = "stage337X_open_run337Y_actual_source_age_proxy_mt5_tester_repair_inputs_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337X_input_review_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337W_DIR = STAGE_DIR / "02_runs" / "run337W"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
REPORT_PATH = REVIEWS_DIR / "run337X_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337X_input_review.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

W_FINAL = RUN337W_DIR / "final_decision.json"
W_GATE_AUDIT = RUN337W_DIR / "required_gate_coverage_audit.csv"
W_SOURCE_AGE = RUN337W_DIR / "source_age_and_availability_audit.csv"
W_FEATURE_BOUNDARY = RUN337W_DIR / "feature_label_boundary_audit.csv"
W_SOURCE_DECISION = RUN337W_DIR / "source_clean_repair_decision.csv"
W_COST_LADDER = RUN337W_DIR / "cost_ladder_contract.csv"
W_DIRECTION_GATE = RUN337W_DIR / "direction_curve_gate_template.csv"
W_PROXY_TEMPLATE = RUN337W_DIR / "proxy_expected_template.csv"
W_PROXY_SCHEMA = RUN337W_DIR / "timestamp_aligned_proxy_mt5_difference_schema.csv"
W_USABILITY = RUN337W_DIR / "usability_decision_rule.csv"
W_TESTER_PLAN = RUN337W_DIR / "tester_boundary_repair_plan.csv"
W_TESTER_GATE = RUN337W_DIR / "tester_feature_last_reach_gate.csv"
W_MODEL_FIREWALL = RUN337W_DIR / "model_validation_firewall.csv"
W_THRESHOLD = RUN337W_DIR / "no_forward_threshold_search_contract.csv"
W_WFO_SPLIT = RUN337W_DIR / "wfo_split_plan.csv"
W_MANIFEST = RUN337W_DIR / "run_manifest.json"

GATE_REVIEW_CSV = RUN_DIR / "gate_review.csv"
EVIDENCE_MATURITY_CSV = RUN_DIR / "evidence_maturity.csv"
CLAIM_MATRIX_CSV = RUN_DIR / "claim_matrix.csv"
GAP_REGISTER_CSV = RUN_DIR / "gap_register.csv"
RUN337Y_QUEUE_CSV = RUN_DIR / "run337Y_queue.csv"
INPUT_HASHES_CSV = RUN_DIR / "input_hashes.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"
DATA_RECEIPT_JSON = RUN_DIR / "data_receipt.json"
RUNTIME_RECEIPT_JSON = RUN_DIR / "runtime_receipt.json"
MODEL_RECEIPT_JSON = RUN_DIR / "model_receipt.json"
JUDGMENT_RECEIPT_JSON = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT_JSON = RUN_DIR / "lineage_receipt.json"

INPUT_FILES = [
    W_FINAL,
    W_GATE_AUDIT,
    W_SOURCE_AGE,
    W_FEATURE_BOUNDARY,
    W_SOURCE_DECISION,
    W_COST_LADDER,
    W_DIRECTION_GATE,
    W_PROXY_TEMPLATE,
    W_PROXY_SCHEMA,
    W_USABILITY,
    W_TESTER_PLAN,
    W_TESTER_GATE,
    W_MODEL_FIREWALL,
    W_THRESHOLD,
    W_WFO_SPLIT,
    W_MANIFEST,
]

OUTPUT_FILES = [
    GATE_REVIEW_CSV,
    EVIDENCE_MATURITY_CSV,
    CLAIM_MATRIX_CSV,
    GAP_REGISTER_CSV,
    RUN337Y_QUEUE_CSV,
    INPUT_HASHES_CSV,
    FINAL_DECISION_JSON,
    RUN_MANIFEST_JSON,
    DATA_RECEIPT_JSON,
    RUNTIME_RECEIPT_JSON,
    MODEL_RECEIPT_JSON,
    JUDGMENT_RECEIPT_JSON,
    LINEAGE_RECEIPT_JSON,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def path_exists(path: Path) -> bool:
    return path.exists()


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
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_with_bom(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_preserve_bom(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    path.write_text(text, encoding=encoding, newline="\n")
    return path


def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337X inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "final": read_json(W_FINAL),
        "gate_audit": read_csv(W_GATE_AUDIT),
        "source_age": read_csv(W_SOURCE_AGE),
        "feature_boundary": read_csv(W_FEATURE_BOUNDARY),
        "source_decision": read_csv(W_SOURCE_DECISION),
        "cost_ladder": read_csv(W_COST_LADDER),
        "direction_gate": read_csv(W_DIRECTION_GATE),
        "proxy_template": read_csv(W_PROXY_TEMPLATE),
        "proxy_schema": read_csv(W_PROXY_SCHEMA),
        "usability": read_csv(W_USABILITY),
        "tester_plan": read_csv(W_TESTER_PLAN),
        "tester_gate": read_csv(W_TESTER_GATE),
        "model_firewall": read_csv(W_MODEL_FIREWALL),
        "threshold": read_csv(W_THRESHOLD),
        "wfo_split": read_csv(W_WFO_SPLIT),
        "manifest": read_json(W_MANIFEST),
    }


def review_gates(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    maturity_by_gate = {
        "source_age_and_availability": ("present_contract_pending_measurement", "source timestamps and max-age buckets are not measured yet"),
        "feature_label_boundary": ("present_contract_ready_for_negative_control", "boundary contract exists but negative control has not run"),
        "source_clean_repair_decision": ("present_contract_ready", "m48/c56 repair and u42 control roles are separated"),
        "cost_ladder_contract": ("present_contract_ready", "cost points and pass/fail rules exist"),
        "direction_curve_gate": ("present_contract_ready", "direction/curve/regime axes are named"),
        "proxy_expected_template": ("present_contract_pending_values", "proxy expected values are templates, not actual row-level values"),
        "proxy_mt5_difference_schema": ("present_contract_pending_runtime_values", "schema exists but MT5 runtime values are absent"),
        "usability_decision_rule": ("present_contract_ready", "claim downgrade rules exist"),
        "tester_boundary_repair_plan": ("present_contract_ready_for_probe", "repair plan exists but latest tester probe is not run in run337X"),
        "tester_feature_last_reach_gate": ("present_blocking_gap", "tester still must reach feature_last before forward judgment"),
        "model_validation_firewall": ("present_contract_ready", "training firewall exists"),
        "no_forward_threshold_search": ("present_contract_ready", "forward threshold retuning ban exists"),
        "wfo_split_plan": ("present_contract_pending_split_manifest", "split plan exists but split membership audit is not run"),
    }
    rows: list[dict[str, Any]] = []
    for gate in inputs["gate_audit"]:
        gate_name = gate.get("gate_name", "")
        maturity, reason = maturity_by_gate.get(gate_name, ("present_review_required", "review required"))
        rows.append(
            {
                "gate_name": gate_name,
                "run337W_status": gate.get("status", ""),
                "row_count": gate.get("row_count", ""),
                "maturity_status": maturity,
                "review_reason": reason,
                "evidence_path": gate.get("evidence_path", ""),
                "allows_training": maturity in {"present_contract_ready"} and gate_name in {"model_validation_firewall", "no_forward_threshold_search"},
                "allows_forward_decision": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_evidence_maturity(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = inputs["source_age"]
    source_pending = sum(1 for row in source_rows if "pending" in row.get("availability_status", ""))
    tester_gate = inputs["tester_gate"][0] if inputs["tester_gate"] else {}
    tester_status = tester_gate.get("current_status", "missing")
    proxy_rows = inputs["proxy_template"]
    proxy_actual_ready = sum(1 for row in proxy_rows if "computed_by_python_proxy" not in json.dumps(row))
    maturity = [
        {
            "evidence_area": "source_age",
            "available_rows": len(source_rows),
            "ready_rows": len(source_rows) - source_pending,
            "missing_or_pending_rows": source_pending,
            "maturity_judgment": "pending_measurement",
            "blocks": "model_training;forward_pass_fail;source_policy_repair_acceptance",
            "next_required_evidence": "source_timestamp_snapshot.csv;source_age_decision.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_area": "proxy_expected_values",
            "available_rows": len(proxy_rows),
            "ready_rows": proxy_actual_ready,
            "missing_or_pending_rows": len(proxy_rows) - proxy_actual_ready,
            "maturity_judgment": "template_only",
            "blocks": "runtime_usability;KPI_authority",
            "next_required_evidence": "proxy_expected_values.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_area": "proxy_mt5_difference",
            "available_rows": len(inputs["proxy_schema"]),
            "ready_rows": 0,
            "missing_or_pending_rows": len(inputs["proxy_schema"]),
            "maturity_judgment": "schema_only_no_runtime_values",
            "blocks": "runtime_signal_parity;forward_decision",
            "next_required_evidence": "timestamp_aligned_proxy_mt5_difference.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_area": "tester_feature_last_reach",
            "available_rows": len(inputs["tester_gate"]),
            "ready_rows": 0 if "blocked" in tester_status else 1,
            "missing_or_pending_rows": 1 if "blocked" in tester_status else 0,
            "maturity_judgment": tester_status,
            "blocks": tester_gate.get("blocks_claim", "Forward Passed;Forward Failed;runtime_authority;Goal Achieve"),
            "next_required_evidence": "tester_history_snapshot.csv;tester_feature_last_gap_report.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_area": "cost_direction_curve",
            "available_rows": len(inputs["cost_ladder"]) + len(inputs["direction_gate"]),
            "ready_rows": len(inputs["cost_ladder"]) + len(inputs["direction_gate"]),
            "missing_or_pending_rows": 0,
            "maturity_judgment": "contract_ready_no_new_kpi",
            "blocks": "ONNX_ready_until_actual branch results exist",
            "next_required_evidence": "branch_preflight_matrix.csv;cost_curve_direction_review.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_area": "model_validation_firewall",
            "available_rows": len(inputs["model_firewall"]) + len(inputs["threshold"]) + len(inputs["wfo_split"]),
            "ready_rows": len(inputs["model_firewall"]) + len(inputs["threshold"]) + len(inputs["wfo_split"]),
            "missing_or_pending_rows": 0,
            "maturity_judgment": "contract_ready_blocks_shortcuts",
            "blocks": "training if source/proxy/tester evidence remains missing",
            "next_required_evidence": "split_membership_audit.csv;negative_control_result.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return maturity


def claim_matrix() -> list[dict[str, Any]]:
    return [
        {
            "claim": "input_contract_completeness",
            "current_decision": "allowed",
            "reason": "run337W produced all required contracts and run337X reviewed maturity",
            "forbidden_extension": "treat contract completeness as model quality",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim": "model_training",
            "current_decision": "blocked_by_evidence_maturity",
            "reason": "source age measurement, split membership audit, and negative controls are not actual evidence yet",
            "forbidden_extension": "train new ONNX before source/as-of firewall is measured",
            "next_condition": "run337Y actual source age and split audit inputs",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim": "runtime_signal_parity",
            "current_decision": "blocked_by_missing_runtime_values",
            "reason": "proxy-MT5 difference schema exists, but actual proxy expected and MT5 telemetry values are not produced in run337X",
            "forbidden_extension": "use proxy-only values as runtime authority",
            "next_condition": "timestamp_aligned_proxy_mt5_difference.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim": "Forward Passed/Failed",
            "current_decision": "blocked_by_tester_feature_last_gap",
            "reason": "tester feature_last reach gate is blocked_tester_gap_remains",
            "forbidden_extension": "judge unseen latest forward bars",
            "next_condition": "tester_last_observed_bar_time >= feature_latest_timestamp",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim": "ONNX_ready_or_goal_achieve",
            "current_decision": "not_allowed",
            "reason": "no new model, no MT5 run, no actual KPI review, no curve quality proof",
            "forbidden_extension": "declare readiness from materialized review",
            "next_condition": "future branch results with cost, curve, direction, runtime parity, and data integrity evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gap_register(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "source_age_actual_measurement_missing",
            "severity": "hard_blocker_before_training",
            "evidence_now": rel(W_SOURCE_AGE),
            "gap": "availability_status remains pending for VIX, USDX, US10YR, mega-cap equities, and US100 broker M5",
            "effect": "원천 시점이 확인되기 전에는 look-ahead bias(미래참조 편향)를 배제할 수 없다.",
            "repair_or_probe": "materialize source timestamp snapshot and source age decision",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "proxy_expected_actual_values_missing",
            "severity": "runtime_parity_blocker",
            "evidence_now": rel(W_PROXY_TEMPLATE),
            "gap": "proxy expected fields are templates, not row-level values",
            "effect": "프록시와 MT5 차이를 숫자로 판단할 수 없다.",
            "repair_or_probe": "produce proxy_expected_values.csv for each attempt and timestamp",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "mt5_runtime_difference_missing",
            "severity": "runtime_parity_blocker",
            "evidence_now": rel(W_PROXY_SCHEMA),
            "gap": "difference schema exists but no MT5 runtime probe result is attached",
            "effect": "런타임 활용성 판단이 signal sanity(신호 점검) 이상으로 올라갈 수 없다.",
            "repair_or_probe": "run or prepare narrow MT5 reprobe with timestamp-aligned difference file",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "tester_feature_last_gap_remains",
            "severity": "forward_decision_blocker",
            "evidence_now": rel(W_TESTER_GATE),
            "gap": "tester_last_observed_bar_time must be measured and reach feature_latest_timestamp",
            "effect": "최신 forward 구간을 못 본 결과로 통과/실패를 말하지 않는다.",
            "repair_or_probe": "tester history snapshot, rollover reprobe, and gap report",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gap_id": "split_membership_and_negative_control_missing",
            "severity": "overfit_firewall_blocker",
            "evidence_now": rel(W_WFO_SPLIT),
            "gap": "WFO split plan exists but split membership and source-shift negative control are not run",
            "effect": "forward data 재튜닝이나 원천 시점 누수를 아직 실제로 걸러내지 못한다.",
            "repair_or_probe": "split_membership_audit.csv and negative_control_result.csv",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def run337y_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337Y_01_source_timestamp_snapshot",
            "task": "materialize actual source timestamp, age bucket, and availability rows for VIX, USDX, US10YR, mega-cap equities, and US100 broker M5",
            "required_inputs": f"{rel(W_SOURCE_AGE)};{rel(W_FEATURE_BOUNDARY)}",
            "required_outputs": "source_timestamp_snapshot.csv;source_age_decision.csv;source_gap_blocker_report.csv",
            "blocked_if_missing": "source timestamp cannot be proven <= US100 decision bar close",
            "effect": "원천 데이터가 forward bar 이후 값을 몰래 쓰는지 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337Y_02_proxy_expected_values",
            "task": "materialize row-level proxy expected values before any MT5 usability claim",
            "required_inputs": f"{rel(W_PROXY_TEMPLATE)};{rel(W_PROXY_SCHEMA)}",
            "required_outputs": "proxy_expected_values.csv;proxy_value_identity.csv",
            "blocked_if_missing": "proxy values cannot be tied to timestamp, attempt, and feature handoff",
            "effect": "프록시 예상값과 MT5 값의 차이를 실제 숫자로 비교할 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337Y_03_mt5_runtime_reprobe_package",
            "task": "materialize or run narrow MT5 runtime reprobe package that can fill the timestamp-aligned difference file",
            "required_inputs": f"{rel(W_TESTER_PLAN)};{rel(W_TESTER_GATE)}",
            "required_outputs": "mt5_reprobe_manifest.json;tester_history_snapshot.csv;timestamp_aligned_proxy_mt5_difference.csv",
            "blocked_if_missing": "Strategy Tester cannot reach feature_last and no repair action is recorded",
            "effect": "런타임 동등성 주장을 proxy-only(프록시 전용)에서 끌어올릴 수 있는지 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337Y_04_split_and_negative_control",
            "task": "materialize split membership audit and source timestamp negative control before training",
            "required_inputs": f"{rel(W_WFO_SPLIT)};{rel(W_THRESHOLD)}",
            "required_outputs": "split_membership_audit.csv;negative_control_result.csv;threshold_identity_audit.csv",
            "blocked_if_missing": "forward rows or shifted source timestamps cannot be identified",
            "effect": "과적합을 위한 또 다른 과적합 경로를 학습 전에 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337Y_05_cost_direction_curve_preflight",
            "task": "materialize branch preflight matrix for cost, direction, curve, and density-preserving probes",
            "required_inputs": f"{rel(W_COST_LADDER)};{rel(W_DIRECTION_GATE)};{rel(W_MODEL_FIREWALL)}",
            "required_outputs": "branch_preflight_matrix.csv;cost_curve_direction_required_outputs.csv",
            "blocked_if_missing": "branch success/failure criteria cannot be evaluated without post-hoc filtering",
            "effect": "좋은 숫자 하나로 깨진 방향/곡선 포켓을 숨기지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def input_hashes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "path": rel(path),
                "exists": path_exists(path),
                "sha256_lf": sha256_lf(path) if path_exists(path) and path.is_file() else "",
                "role": "run337W_input",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    payloads = [
        (
            DATA_RECEIPT_JSON,
            {
                "receipt_type": "data_integrity(데이터 무결성)",
                "run_id": RUN_ID,
                "data_source": [rel(W_SOURCE_AGE), rel(W_FEATURE_BOUNDARY), rel(W_TESTER_GATE)],
                "time_axis": "US100 M5 UTC bar close; external source timestamp must be <= decision bar close",
                "sample_scope": "Stage337 repair-input review only; no new broker bars or training rows consumed",
                "missing_or_duplicate_check": "not_run; run337X reviews contracts and opens run337Y measurement",
                "feature_label_boundary": "contract present, negative control missing",
                "split_boundary": "WFO split plan present, split membership audit missing",
                "leakage_risk": "source timestamp after decision bar and forward threshold search",
                "data_hash_or_identity": rel(INPUT_HASHES_CSV),
                "integrity_judgment": "usable_with_boundary_for_input_review_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT_JSON,
            {
                "receipt_type": "runtime_parity(런타임 동등성)",
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "not_run_in_run337X",
                "shared_contract": rel(W_PROXY_SCHEMA),
                "known_differences": "proxy expected values and MT5 runtime values are missing; tester gap remains",
                "parity_check": "contract review only; no runtime execution",
                "parity_identity": rel(INPUT_HASHES_CSV),
                "runtime_claim_boundary": "research-only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT_JSON,
            {
                "receipt_type": "model_validation(모델 검증)",
                "run_id": RUN_ID,
                "model_family": "not_trained_in_run337X",
                "target_and_label": "not_applicable; feature-label boundary contract reviewed",
                "split_method": "WFO plan reviewed; split membership audit missing",
                "selection_metric": "not_applicable_no_selection",
                "secondary_metrics": "cost ladder, direction/curve/regime gates are predeclared",
                "threshold_policy": "fixed_no_forward_search",
                "overfit_risk": "source timestamp leakage; proxy-only authority; tester partial forward; forward threshold tuning",
                "calibration_risk": "scores remain diagnostic until actual proxy/MT5 and calibration evidence exist",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "blocked_for_training_allowed_for_input_review",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT_JSON,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "run_id": RUN_ID,
                "result_subject": "run337W materialized repair inputs",
                "evidence_available": metrics,
                "evidence_missing": "actual source timestamps, proxy expected values, MT5 runtime values, split membership audit, tester feature_last reach",
                "judgment_label": "exploratory_input_review",
                "claim_boundary": "input contracts complete; training/forward/runtime/goal claims forbidden",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "입력 양식은 갖췄지만 실제 측정값이 없어 다음은 측정 패키지다.",
                "claim_boundary_full": CLAIM_BOUNDARY,
            },
        ),
        (
            LINEAGE_RECEIPT_JSON,
            {
                "receipt_type": "artifact_lineage(산출물 계보)",
                "run_id": RUN_ID,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": rel(INPUT_HASHES_CSV),
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked reports and script; local 02_runs outputs ignored_with_manifest",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload | {"generated_at_utc": generated_at}) for path, payload in payloads]


def write_report(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337X Input Review(337X 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- model training(모델 학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Review Counts(검토 수치)

- gate rows reviewed(검토 게이트 행): `{metrics['gate_rows_reviewed']}`
- gate contracts present(게이트 계약 존재): `{metrics['gate_contracts_present']}`
- hard blockers(강한 차단 요소): `{metrics['hard_blocker_count']}`
- run337Y queue rows(337Y 대기열 행): `{metrics['queue_rows']}`
- input files hashed(해시 입력 파일): `{metrics['input_hash_rows']}`

## Read(판독)

run337X(337X 실행)는 run337W(337W 실행)의 계약 파일이 구조적으로 빠짐없이 존재하는지 확인했다. 효과(effect, 효과)는 source age(원천 나이), proxy expected values(프록시 예상값), MT5 runtime values(MT5 런타임 값), tester feature_last reach(테스터 피처 끝 도달), split membership(분할 소속)이 실제 증거인지 템플릿인지 분리한 것이다.

결론은 `input_contracts_complete_but_evidence_maturity_blocks_training_forward_runtime_claims`다. 즉 입력 계약은 다음 실행을 만들 만큼 충분하지만, model training(모델 학습), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 금지된다. 다음은 run337Y(337Y 실행)에서 실제 source timestamp snapshot(원천 시점 스냅샷), proxy expected values(프록시 예상값), MT5 runtime difference(MT5 런타임 차이), split/negative control(분할/부정 대조)을 물질화하는 것이다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337X Decision(337X 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- hard_blockers(강한 차단 요소): `{metrics['hard_blocker_count']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337X(337X 실행)는 run337W(337W 실행)의 materialized inputs(물질화 입력)을 검토해 계약은 완성됐지만 실제 측정 증거가 부족하다고 판정했다. 다음 최소 조건은 run337Y(337Y 실행)에서 source age(원천 나이), proxy-MT5 actual difference(프록시-MT5 실제 차이), tester reach(테스터 도달), split/negative control(분할/부정 대조)을 실제 파일로 만드는 것이다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- input_contracts_complete(입력 계약 완성): `{metrics['gate_contracts_present']}/{metrics['gate_rows_reviewed']}`
- hard_blockers(강한 차단 요소): `{metrics['hard_blocker_count']}`
- evidence_gap_summary(증거 공백 요약): `source_age_pending;proxy_values_missing;mt5_runtime_difference_missing;tester_gap_remains;split_negative_control_missing`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last before Forward Passed/Failed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337X는 입력 계약을 검토했고, 실제 측정 증거가 부족해 run337Y 측정 패키지를 연다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection_text))

    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_with_bom(STAGE_BRIEF)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("- latest_run("):
                lines[index] = f"- latest_run(최신 실행): `{RUN_ID}`"
        text = "\n".join(lines) + "\n"
        if "run337W_summary(337W 요약)" not in text:
            text = text.replace(
                "- run337M_summary(337M 요약):",
                "- run337W_summary(337W 요약): `completed_stage337W_cost_buffer_source_policy_repair_inputs_materialized_no_training_no_mt5`. Effect(효과): 비용/원천/프록시-MT5/테스터/모델 검증 입력 계약을 물질화했다.\n- run337X_summary(337X 요약): `completed_stage337X_materialized_inputs_review_evidence_gaps_bound_no_training_no_mt5`. Effect(효과): 입력 계약은 완성됐지만 실제 측정 증거 부족으로 run337Y 측정 패키지를 연다.\n- run337M_summary(337M 요약):",
                1,
            )
        elif "run337X_summary(337X 요약)" not in text:
            text = text.replace(
                "- selected_candidate(선택 후보):",
                "- run337X_summary(337X 요약): `completed_stage337X_materialized_inputs_review_evidence_gaps_bound_no_training_no_mt5`. Effect(효과): 입력 계약은 완성됐지만 실제 측정 증거 부족으로 run337Y 측정 패키지를 연다.\n- selected_candidate(선택 후보):",
                1,
            )
        artifacts.append(write_text_preserve_bom(STAGE_BRIEF, text, had_bom))

    focus_entry = (
        "- >-\n"
        f"  Stage337 run337X focus complete: Stage337(337단계) run337X(337X 실행)는 `{STATUS}`로 run337W 입력 계약을 검토했다. "
        f"Effect(효과): gate contracts(게이트 계약) `{metrics['gate_contracts_present']}/{metrics['gate_rows_reviewed']}`는 존재하지만 source/proxy/MT5/tester/split evidence(원천/프록시/MT5/테스터/분할 증거)가 부족해 run337Y(337Y 실행) 실제 측정 패키지를 연다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_with_bom(WORKSPACE_STATE)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[index] = f"current_run_id: {NEXT_RUN_ID}"
            if line.startswith("updated_on:"):
                lines[index] = f"updated_on: '{TODAY}'"
        text = "\n".join(lines) + "\n"
        if "Stage337 run337X focus complete" not in text and "current_focus:\n" in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus_entry + "\n", 1)
        artifacts.append(write_text_preserve_bom(WORKSPACE_STATE, text, had_bom))

    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_with_bom(CURRENT_STATE)
        entry = f"""
## Stage337 run337X(337X 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337W 입력 계약 `{metrics['gate_contracts_present']}/{metrics['gate_rows_reviewed']}`개를 검토했고, source/proxy/MT5/tester/split(원천/프록시/MT5/테스터/분할) 실제 증거가 부족해 학습/전진/런타임/목표 주장을 금지한다.
"""
        if "## Stage337 run337X(337X 실행)" not in text:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        artifacts.append(write_text_preserve_bom(CURRENT_STATE, text, had_bom))

    if path_exists(CHANGELOG):
        text, had_bom = read_text_with_bom(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337X(337X 실행) `{STATUS}`. Effect(효과): 입력 계약은 검토 완료, 실제 증거 부족으로 run337Y 측정 패키지를 열었고 Forward/Goal(전진/목표) 주장은 없음."
        if "Stage337 run337X(337X 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        artifacts.append(write_text_preserve_bom(CHANGELOG, text, had_bom))
    return artifacts


def append_artifact_rows(paths: Sequence[Path], generated_at: str) -> Path:
    existing = read_csv(ARTIFACT_REGISTRY)
    columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_ids = {f"{RUN_ID}::{rel(path)}" for path in paths}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    for path in paths:
        if not path_exists(path) or not path.is_file():
            continue
        suffix = path.suffix.lower().lstrip(".") or "file"
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix,
                "path": rel(path),
                "sha256": sha256_lf(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at,
                "notes": STATUS,
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def update_registers(artifact_paths: Sequence[Path], metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    paths = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "review_runtime_parity_model_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};hard_blockers={metrics['hard_blocker_count']};goal_achieve_not_claimed.",
                "family": "materialized_repair_input_review",
                "primary_report": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "ledger_row_id": f"{RUN_ID}__materialized_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "review_runtime_parity_model_validation",
                "evidence_scope": "run337W materialized input contracts",
                "kpi_scope": "input_review_no_new_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};hard_blockers={metrics['hard_blocker_count']};goal_achieve_not_claimed.",
                "decision": DECISION,
                "run_key": f"{RUN_ID}__materialized_input_review",
                "family": "materialized_repair_input_review",
                "question": "do run337W contracts permit training forward or runtime claims",
                "metric_scope": "input_contract_review_only_no_forward_decision",
                "primary_artifact": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            ALPHA_LEDGER,
            ["ledger_row_id"],
            {
                "ledger_row_id": f"{RUN_ID}__input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "input_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "contract_maturity_and_evidence_gap_review",
                "tier_scope": "out_of_scope_by_claim_no_tier_kpi",
                "kpi_scope": "no_new_kpi_input_review",
                "scoreboard_lane": "review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": "not_applicable",
                "guardrail_kpi": "source_age;proxy_mt5;tester_feature_last;split_negative_control",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
    ]
    paths.append(append_artifact_rows([*artifact_paths, Path(__file__)], generated_at))
    return paths


def main() -> int:
    generated_at = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()

    gate_rows = review_gates(inputs)
    maturity_rows = review_evidence_maturity(inputs)
    claim_rows = claim_matrix()
    gap_rows = gap_register(inputs)
    queue_rows = run337y_queue()
    hash_rows = input_hashes()

    hard_blockers = [row for row in gap_rows if "blocker" in row["severity"]]
    metrics = {
        "gate_rows_reviewed": len(gate_rows),
        "gate_contracts_present": sum(1 for row in gate_rows if row["run337W_status"] == "present"),
        "evidence_maturity_rows": len(maturity_rows),
        "hard_blocker_count": len(hard_blockers),
        "claim_rows": len(claim_rows),
        "gap_rows": len(gap_rows),
        "queue_rows": len(queue_rows),
        "input_hash_rows": len(hash_rows),
    }

    artifact_paths: list[Path] = [
        write_csv(GATE_REVIEW_CSV, ["gate_name", "run337W_status", "row_count", "maturity_status", "review_reason", "evidence_path", "allows_training", "allows_forward_decision", "claim_boundary"], gate_rows),
        write_csv(EVIDENCE_MATURITY_CSV, ["evidence_area", "available_rows", "ready_rows", "missing_or_pending_rows", "maturity_judgment", "blocks", "next_required_evidence", "claim_boundary"], maturity_rows),
        write_csv(CLAIM_MATRIX_CSV, ["claim", "current_decision", "reason", "forbidden_extension", "next_condition", "claim_boundary"], claim_rows),
        write_csv(GAP_REGISTER_CSV, ["gap_id", "severity", "evidence_now", "gap", "effect", "repair_or_probe", "next_run", "claim_boundary"], gap_rows),
        write_csv(RUN337Y_QUEUE_CSV, ["queue_id", "task", "required_inputs", "required_outputs", "blocked_if_missing", "effect", "claim_boundary"], queue_rows),
        write_csv(INPUT_HASHES_CSV, ["path", "exists", "sha256_lf", "role", "claim_boundary"], hash_rows),
    ]
    artifact_paths.extend(write_receipts(metrics, generated_at))
    artifact_paths.append(write_report(metrics))
    artifact_paths.append(write_decision_doc(metrics))
    artifact_paths.extend(update_status_docs(metrics))

    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        **metrics,
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(FINAL_DECISION_JSON, final_decision))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST_JSON,
            {
                **final_decision,
                "generated_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "artifacts": [rel(path) for path in [*artifact_paths, RUN_MANIFEST_JSON] if path_exists(path) or path == RUN_MANIFEST_JSON],
            },
        )
    )
    artifact_paths.extend(update_registers(artifact_paths, metrics, generated_at))

    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
