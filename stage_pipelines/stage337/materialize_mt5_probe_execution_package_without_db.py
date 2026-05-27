from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_bounded_measurement_harness_without_db as bj


aw = bj.aw

TODAY = "2026-05-27"
STAGE_ID = bj.STAGE_ID
RUN_NUMBER = "run337BK"
RUN_ID = "run337BK_materialize_mt5_probe_execution_package_without_db_v1"
PARENT_RUN_ID = bj.RUN_ID
NEXT_RUN_ID = "run337BL_review_mt5_probe_execution_package_without_db_v1"
STATUS = "completed_stage337BK_mt5_probe_execution_package_materialized_no_training_no_selection_no_mt5_execution"
JUDGMENT = "mt5_probe_execution_package_materialized_for_review_with_feature_last_proxy_profit_forensics_contracts"
DECISION = "stage337BK_open_run337BL_review_mt5_probe_execution_package_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BK_mt5_probe_execution_package_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bj.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
REVIEWS_DIR = bj.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BK_mt5_probe_execution_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BK_mt5_probe_execution_package.md"
SELECTED_STATUS = bj.SELECTED_STATUS
STAGE_BRIEF = bj.STAGE_BRIEF
WORKSPACE_STATE = bj.WORKSPACE_STATE
CURRENT_STATE = bj.CURRENT_STATE
CHANGELOG = bj.CHANGELOG
RUN_REGISTRY = bj.RUN_REGISTRY
ALPHA_LEDGER = bj.ALPHA_LEDGER
ARTIFACT_REGISTRY = bj.ARTIFACT_REGISTRY
STAGE_LEDGER = bj.STAGE_LEDGER

RUN337BJ_DIR = STAGE_DIR / "02_runs" / "run337BJ"
BJ_FINAL = RUN337BJ_DIR / "final_decision.json"
BJ_MANIFEST = RUN337BJ_DIR / "run_manifest.json"
BJ_COMPONENT_REVIEW = RUN337BJ_DIR / "measurement_harness_component_review.csv"
BJ_PROFIT_REVIEW = RUN337BJ_DIR / "profit_curve_schema_review.csv"
BJ_PROXY_REVIEW = RUN337BJ_DIR / "proxy_mt5_schema_review.csv"
BJ_MT5_REVIEW = RUN337BJ_DIR / "mt5_probe_manifest_review.csv"
BJ_COST_REVIEW = RUN337BJ_DIR / "cost_stress_review.csv"
BJ_LOT_REVIEW = RUN337BJ_DIR / "lot_normalization_review.csv"
BJ_REGIME_REVIEW = RUN337BJ_DIR / "regime_slice_review.csv"
BJ_LOOKAHEAD_REVIEW = RUN337BJ_DIR / "no_lookahead_validation_review.csv"
BJ_EXECUTION_PLAN_REVIEW = RUN337BJ_DIR / "measurement_execution_plan_review.csv"
BJ_HANDOFF = RUN337BJ_DIR / "mt5_probe_package_handoff_boundary.csv"
BJ_QUEUE = RUN337BJ_DIR / "run337BK_mt5_probe_package_queue.csv"
BJ_GATE_AUDIT = RUN337BJ_DIR / "required_gate_coverage_audit.csv"
BJ_EXPERIMENT_RECEIPT = RUN337BJ_DIR / "experiment_design_receipt.json"
BJ_DATA_RECEIPT = RUN337BJ_DIR / "data_integrity_receipt.json"
BJ_MODEL_RECEIPT = RUN337BJ_DIR / "model_validation_receipt.json"
BJ_RUNTIME_RECEIPT = RUN337BJ_DIR / "runtime_parity_receipt.json"
BJ_PERFORMANCE_RECEIPT = RUN337BJ_DIR / "performance_attribution_receipt.json"
BJ_ARTIFACT_RECEIPT = RUN337BJ_DIR / "artifact_lineage_receipt.json"
BJ_JUDGMENT_RECEIPT = RUN337BJ_DIR / "result_judgment_receipt.json"

STAGE323_ADAPTER_MANIFEST = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
    / "adapter_package_manifest.json"
)
STAGE323_RUNTIME_FEATURE_ORDER = STAGE323_ADAPTER_MANIFEST.parent / "feature_order_runtime.csv"
STAGE323_DECISION_SURFACE = STAGE323_ADAPTER_MANIFEST.parent / "decision_surface.json"
STAGE323_RISK_LOGIC = STAGE323_ADAPTER_MANIFEST.parent / "risk_logic.json"
STAGE323_RUNTIME_HANDOFF = STAGE323_ADAPTER_MANIFEST.parent / "runtime_handoff_manifest.json"
STAGE325_RUN_MANIFEST = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "run_manifest.json"
)
STAGE325_FEATURE_ORDER_RECEIPT = STAGE325_RUN_MANIFEST.parent / "feature_order_parity_receipt.json"
STAGE325_ONNX_PARITY_RECEIPT = STAGE325_RUN_MANIFEST.parent / "onnx_parity_receipt.json"
STAGE325_RUNTIME_PARITY_RECEIPT = STAGE325_RUN_MANIFEST.parent / "runtime_parity_receipt.json"
STAGE328_SIGNAL_CONTRACT = (
    ROOT
    / "stages"
    / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
    / "02_runs"
    / "run328A"
    / "frozen_signal_contract.json"
)
STAGE328B_DECISION_REPORT = (
    ROOT
    / "stages"
    / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
    / "03_reviews"
    / "final_stage328B_decision_report.md"
)
RUN337AN_DECISION_MATRIX = STAGE_DIR / "02_runs" / "run337AN" / "broker_rollover_reprobe_decision_matrix.csv"
RUN337AN_FEATURE_AUDIT = STAGE_DIR / "02_runs" / "run337AN" / "feature_last_timestamp_audit.csv"

EA_ENTRYPOINT = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
EA_INCLUDE_DIR = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime"
TERMINAL_PATH = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/terminal64.exe")
TERMINAL_DATA_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
TESTER_PROFILE_ROOT = TERMINAL_DATA_ROOT / "MQL5" / "Profiles" / "Tester"
COMMON_FILES_ROOT = Path("C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/Common/Files")

MT5_PROBE_EXECUTION_MANIFEST = RUN_DIR / "mt5_probe_execution_manifest.csv"
FROZEN_SUBJECT_IDENTITY = RUN_DIR / "frozen_subject_identity.csv"
TESTER_COMMAND_CHECKLIST = RUN_DIR / "tester_command_checklist.csv"
RUNTIME_FILE_HANDOFF_MANIFEST = RUN_DIR / "runtime_file_handoff_manifest.csv"
PROXY_MT5_DIFF_OUTPUT_CONTRACT = RUN_DIR / "proxy_mt5_diff_output_contract.csv"
PROFIT_TRADE_OUTPUT_CONTRACT = RUN_DIR / "profit_trade_output_contract.csv"
FEATURE_LAST_GATE_CONTRACT = RUN_DIR / "feature_last_gate_contract.csv"
NO_LOOKAHEAD_RUNTIME_AUDIT_CONTRACT = RUN_DIR / "no_lookahead_runtime_audit_contract.csv"
BACKTEST_FORENSICS_IDENTITY_CONTRACT = RUN_DIR / "backtest_forensics_identity_contract.csv"
COST_STRESS_EXECUTION_CONTRACT = RUN_DIR / "cost_stress_execution_contract.csv"
LOT_NORMALIZED_EXECUTION_CONTRACT = RUN_DIR / "lot_normalized_execution_contract.csv"
REGIME_ATTRIBUTION_EXECUTION_CONTRACT = RUN_DIR / "regime_attribution_execution_contract.csv"
ROUTE_SIGNAL_HANDOFF_STATUS = RUN_DIR / "route_signal_handoff_status.csv"
REFERENCE_SCOUT_RECEIPT = RUN_DIR / "reference_scout_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ENVIRONMENT_RECEIPT = RUN_DIR / "environment_reproducibility_receipt.json"
CLAIM_DISCIPLINE_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
RUN337BL_QUEUE = RUN_DIR / "run337BL_review_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
TESTER_INI_TEMPLATE = MT5_DIR / "run337BK_cp322a_forward_probe_review_template.ini"
TESTER_SET_TEMPLATE = MT5_DIR / "run337BK_cp322a_forward_probe_review_template.set"

INPUT_FILES = (
    BJ_FINAL,
    BJ_MANIFEST,
    BJ_COMPONENT_REVIEW,
    BJ_PROFIT_REVIEW,
    BJ_PROXY_REVIEW,
    BJ_MT5_REVIEW,
    BJ_COST_REVIEW,
    BJ_LOT_REVIEW,
    BJ_REGIME_REVIEW,
    BJ_LOOKAHEAD_REVIEW,
    BJ_EXECUTION_PLAN_REVIEW,
    BJ_HANDOFF,
    BJ_QUEUE,
    BJ_GATE_AUDIT,
    BJ_EXPERIMENT_RECEIPT,
    BJ_DATA_RECEIPT,
    BJ_MODEL_RECEIPT,
    BJ_RUNTIME_RECEIPT,
    BJ_PERFORMANCE_RECEIPT,
    BJ_ARTIFACT_RECEIPT,
    BJ_JUDGMENT_RECEIPT,
    STAGE323_ADAPTER_MANIFEST,
    STAGE323_RUNTIME_FEATURE_ORDER,
    STAGE323_DECISION_SURFACE,
    STAGE323_RISK_LOGIC,
    STAGE323_RUNTIME_HANDOFF,
    STAGE325_RUN_MANIFEST,
    STAGE325_FEATURE_ORDER_RECEIPT,
    STAGE325_ONNX_PARITY_RECEIPT,
    STAGE325_RUNTIME_PARITY_RECEIPT,
    STAGE328_SIGNAL_CONTRACT,
    STAGE328B_DECISION_REPORT,
)
OUTPUT_FILES = (
    MT5_PROBE_EXECUTION_MANIFEST,
    FROZEN_SUBJECT_IDENTITY,
    TESTER_COMMAND_CHECKLIST,
    RUNTIME_FILE_HANDOFF_MANIFEST,
    PROXY_MT5_DIFF_OUTPUT_CONTRACT,
    PROFIT_TRADE_OUTPUT_CONTRACT,
    FEATURE_LAST_GATE_CONTRACT,
    NO_LOOKAHEAD_RUNTIME_AUDIT_CONTRACT,
    BACKTEST_FORENSICS_IDENTITY_CONTRACT,
    COST_STRESS_EXECUTION_CONTRACT,
    LOT_NORMALIZED_EXECUTION_CONTRACT,
    REGIME_ATTRIBUTION_EXECUTION_CONTRACT,
    ROUTE_SIGNAL_HANDOFF_STATUS,
    REFERENCE_SCOUT_RECEIPT,
    RUN_EVIDENCE_RECEIPT,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    DATA_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    ENVIRONMENT_RECEIPT,
    CLAIM_DISCIPLINE_RECEIPT,
    RUN337BL_QUEUE,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    TESTER_INI_TEMPLATE,
    TESTER_SET_TEMPLATE,
)

MANIFEST_COLUMNS = (
    "probe_id",
    "probe_role",
    "frozen_subject",
    "symbol",
    "timeframe",
    "tester_model",
    "from_date",
    "to_date",
    "feature_last_required_utc",
    "api_latest_observed_utc",
    "tester_last_observed_bar_time",
    "terminal_path",
    "terminal_exists",
    "terminal_data_root",
    "terminal_data_root_exists",
    "ea_entrypoint",
    "ea_entrypoint_sha256",
    "include_module_hashes",
    "onnx_recorded_path",
    "onnx_recorded_sha256",
    "onnx_local_path",
    "onnx_local_sha256",
    "adapter_manifest_path",
    "feature_order_hash",
    "set_template_path",
    "ini_template_path",
    "expected_report_path",
    "expected_telemetry_path",
    "expected_summary_path",
    "expected_trade_list_path",
    "execution_readiness_status",
    "effect",
    "claim_boundary",
)
IDENTITY_COLUMNS = (
    "identity_id",
    "identity_subject",
    "source_path",
    "source_sha256",
    "source_status",
    "frozen_value",
    "must_preserve",
    "effect",
    "claim_boundary",
)
CHECKLIST_COLUMNS = (
    "step_id",
    "sequence",
    "action",
    "required_input",
    "expected_output",
    "pass_condition",
    "fail_condition",
    "effect",
    "claim_boundary",
)
HANDOFF_COLUMNS = (
    "handoff_id",
    "file_role",
    "repo_template_path",
    "terminal_expected_path",
    "common_files_expected_path",
    "required_before_runtime",
    "required_after_runtime",
    "validation_rule",
    "effect",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "field_name",
    "field_type",
    "required",
    "source",
    "validation_rule",
    "downstream_use",
    "forbidden_inference",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def path_status(path: Path) -> str:
    return "exists" if aw.path_exists(path) else "missing"


def maybe_hash(path: Path) -> str:
    return aw.sha256_file(path) if aw.path_exists(path) else "missing"


def rel_or_abs(path: Path) -> str:
    try:
        return aw.rel(path)
    except Exception:
        return path.as_posix()


def first_row_value(rows: Sequence[Mapping[str, str]], key: str, default: str = "") -> str:
    for row in rows:
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return default


def discover_cp322a_onnx() -> tuple[str, str]:
    model_dir = STAGE325_RUN_MANIFEST.parent / "models"
    if not aw.path_exists(model_dir):
        return "", ""
    candidates = sorted(aw.io_path(model_dir).glob("cp322a_route_signal_identity.onnx*"))
    if not candidates:
        return "", ""
    path = candidates[0]
    return rel_or_abs(path), maybe_hash(path)


def include_module_hashes() -> str:
    if not aw.path_exists(EA_INCLUDE_DIR):
        return "include_dir_missing"
    parts = []
    for path in sorted(aw.io_path(EA_INCLUDE_DIR).glob("*.mqh")):
        parts.append(f"{path.name}:{maybe_hash(path)}")
    return "|".join(parts)


def recorded_onnx_identity(stage325: Mapping[str, Any]) -> tuple[str, str]:
    hashes = stage325.get("output_hashes", {})
    if isinstance(hashes, Mapping):
        for path, digest in hashes.items():
            if str(path).endswith("cp322a_route_signal_identity.onnx"):
                return str(path), str(digest)
    return (
        "stages/325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a/02_runs/run325A/models/cp322a_route_signal_identity.onnx",
        "missing_in_manifest",
    )


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BK source files: {missing}")
    an_matrix = read_rows(RUN337AN_DECISION_MATRIX) if aw.path_exists(RUN337AN_DECISION_MATRIX) else []
    an_features = read_rows(RUN337AN_FEATURE_AUDIT) if aw.path_exists(RUN337AN_FEATURE_AUDIT) else []
    return {
        "parent_final": read_json(BJ_FINAL),
        "parent_manifest": read_json(BJ_MANIFEST),
        "parent_gates": read_rows(BJ_GATE_AUDIT),
        "queue": read_rows(BJ_QUEUE),
        "handoff": read_rows(BJ_HANDOFF),
        "adapter_manifest": read_json(STAGE323_ADAPTER_MANIFEST),
        "stage325_manifest": read_json(STAGE325_RUN_MANIFEST),
        "feature_order": read_json(STAGE325_FEATURE_ORDER_RECEIPT),
        "stage328_contract": read_json(STAGE328_SIGNAL_CONTRACT),
        "an_matrix": an_matrix,
        "an_features": an_features,
    }


def build_frozen_identity(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    adapter = src["adapter_manifest"]
    stage325 = src["stage325_manifest"]
    feature_order = src["feature_order"]
    onnx_recorded_path, onnx_recorded_hash = recorded_onnx_identity(stage325)
    onnx_local_path, onnx_local_hash = discover_cp322a_onnx()
    risk = adapter.get("source_handoff_snapshot", {}).get("risk_logic", {})
    rows = [
        (
            "selected_candidate",
            "cp322A_cp321b_exact_replay_control_surface",
            STAGE323_ADAPTER_MANIFEST,
            maybe_hash(STAGE323_ADAPTER_MANIFEST),
            "exists",
            "selected candidate fixed(선택 후보 고정)",
        ),
        (
            "onnx_model",
            f"recorded={onnx_recorded_path};local={onnx_local_path or 'missing'};recorded_hash={onnx_recorded_hash};local_hash={onnx_local_hash or 'missing'}",
            STAGE325_RUN_MANIFEST,
            maybe_hash(STAGE325_RUN_MANIFEST),
            "manifest_recorded_local_checked",
            "ONNX model fixed(온엑스 모델 고정)",
        ),
        (
            "adapter_package",
            str(adapter.get("adapter_package_id", "stage323_cp322a_selected_curve_adapter_package_v1")),
            STAGE323_ADAPTER_MANIFEST,
            maybe_hash(STAGE323_ADAPTER_MANIFEST),
            "exists",
            "Adapter package fixed(어댑터 패키지 고정)",
        ),
        (
            "feature_order",
            f"{feature_order.get('onnx_input_feature_order')} hash={feature_order.get('onnx_input_feature_order_hash')}",
            STAGE325_FEATURE_ORDER_RECEIPT,
            maybe_hash(STAGE325_FEATURE_ORDER_RECEIPT),
            "exists",
            "feature order fixed(피처 순서 고정)",
        ),
        (
            "decision_surface",
            "D/B route signal identity surface, no new D/B rewrite(D/B 경로 신호 정체성 표면, 새 D/B 재작성 없음)",
            STAGE323_DECISION_SURFACE,
            maybe_hash(STAGE323_DECISION_SURFACE),
            path_status(STAGE323_DECISION_SURFACE),
            "D/B decision surface fixed(D/B 판단 표면 고정)",
        ),
        (
            "risk_lot_atr",
            (
                f"fixed_lot={risk.get('fixed_lot', 'unknown')};"
                f"atr_sltp_enabled={risk.get('atr_sltp_enabled', 'unknown')};"
                f"atr_stop_multiplier={risk.get('atr_stop_multiplier', 'unknown')};"
                f"atr_take_profit_multiplier={risk.get('atr_take_profit_multiplier', 'unknown')}"
            ),
            STAGE323_RISK_LOGIC,
            maybe_hash(STAGE323_RISK_LOGIC),
            path_status(STAGE323_RISK_LOGIC),
            "risk, lot, ATR SL/TP fixed(위험/로트/ATR 손절익절 고정)",
        ),
        (
            "runtime_handoff",
            str(adapter.get("runtime_handoff_path", aw.rel(STAGE323_RUNTIME_HANDOFF))),
            STAGE323_RUNTIME_HANDOFF,
            maybe_hash(STAGE323_RUNTIME_HANDOFF),
            path_status(STAGE323_RUNTIME_HANDOFF),
            "runtime handoff fixed(런타임 인계 고정)",
        ),
    ]
    return [
        {
            "identity_id": f"{RUN_NUMBER}_{subject}",
            "identity_subject": subject,
            "source_path": rel_or_abs(source_path),
            "source_sha256": source_hash,
            "source_status": source_status,
            "frozen_value": frozen_value,
            "must_preserve": "true",
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for subject, frozen_value, source_path, source_hash, source_status, effect in rows
    ]


def build_probe_manifest(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    stage325 = src["stage325_manifest"]
    feature_order = src["feature_order"]
    an_matrix = src["an_matrix"]
    an_features = src["an_features"]
    feature_last = first_row_value(an_features, "feature_last_timestamp", "2026-05-27T02:00:00Z")
    api_latest = first_row_value(an_matrix, "api_latest_us100_close_utc", "unknown")
    tester_last = first_row_value(an_matrix, "tester_last_observed_bar_time", "unknown")
    onnx_recorded_path, onnx_recorded_hash = recorded_onnx_identity(stage325)
    onnx_local_path, onnx_local_hash = discover_cp322a_onnx()
    ea_hash = maybe_hash(EA_ENTRYPOINT)
    module_hashes = include_module_hashes()
    probes = [
        (
            "broker_current_day_forward_probe",
            "primary_forward_visibility_probe(주 전진 가시성 탐침)",
            "2026.04.14",
            "latest_available_after_review",
            "blocked_until_run322b_route_signal_forward_handoff_exists",
        ),
        (
            "completed_day_anchor_probe",
            "completed_day_anchor_control(완성일 기준 대조)",
            "2026.04.14",
            "2026.05.26",
            "review_only_anchor_not_forward_authority",
        ),
        (
            "shifted_custom_timestamp_probe",
            "shifted_custom_timestamp_control(이동 커스텀 시각 대조)",
            "2026.04.14",
            "2026.05.26",
            "diagnostic_control_not_forward_authority",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for probe_id, role, from_date, to_date, readiness in probes:
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{probe_id}"
        common_base = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}/{probe_id}"
        rows.append(
            {
                "probe_id": f"{RUN_NUMBER}_{probe_id}",
                "probe_role": role,
                "frozen_subject": "cp322A_cp321b_exact_replay_control_surface",
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": "4_real_ticks(실제 틱)",
                "from_date": from_date,
                "to_date": to_date,
                "feature_last_required_utc": feature_last,
                "api_latest_observed_utc": api_latest,
                "tester_last_observed_bar_time": tester_last,
                "terminal_path": TERMINAL_PATH.as_posix(),
                "terminal_exists": bool_text(TERMINAL_PATH.exists()),
                "terminal_data_root": TERMINAL_DATA_ROOT.as_posix(),
                "terminal_data_root_exists": bool_text(TERMINAL_DATA_ROOT.exists()),
                "ea_entrypoint": aw.rel(EA_ENTRYPOINT),
                "ea_entrypoint_sha256": ea_hash,
                "include_module_hashes": module_hashes,
                "onnx_recorded_path": onnx_recorded_path,
                "onnx_recorded_sha256": onnx_recorded_hash,
                "onnx_local_path": onnx_local_path or "missing",
                "onnx_local_sha256": onnx_local_hash or "missing",
                "adapter_manifest_path": aw.rel(STAGE323_ADAPTER_MANIFEST),
                "feature_order_hash": str(feature_order.get("onnx_input_feature_order_hash", "")),
                "set_template_path": aw.rel(TESTER_SET_TEMPLATE),
                "ini_template_path": aw.rel(TESTER_INI_TEMPLATE),
                "expected_report_path": aw.rel(MT5_DIR / "reports" / f"{report_name}.htm"),
                "expected_telemetry_path": f"{common_base}/telemetry/{probe_id}_telemetry.csv",
                "expected_summary_path": f"{common_base}/telemetry/{probe_id}_summary.csv",
                "expected_trade_list_path": aw.rel(RUN_DIR / "profit_trade_records.csv"),
                "execution_readiness_status": readiness,
                "effect": "binds tester identity before MT5 execution(MT5 실행 전 테스터 정체성을 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tester_templates(src: Mapping[str, Any]) -> list[Path]:
    feature_order = src["feature_order"]
    onnx_recorded_path, _ = recorded_onnx_identity(src["stage325_manifest"])
    common_base = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}/broker_current_day_forward_probe"
    set_text = "\n".join(
        [
            "; generated_by=stage_pipelines.stage337.materialize_mt5_probe_execution_package_without_db",
            f"InpRunId={RUN_ID}",
            "InpExplorationLabel=stage337_cp322A_frozen_forward_probe_review",
            "InpTierLabel=Tier A+B",
            "InpPrimaryActiveTier=tier_a",
            "InpSplitLabel=forward_after_2026_04_14",
            "InpMainSymbol=US100",
            "InpTimeframe=5",
            f"InpModelPath={onnx_recorded_path}",
            "InpModelId=cp322a_route_signal_identity_frozen",
            "InpModelBackend=onnx",
            "InpModelUseCommonFiles=true",
            f"InpFeatureCsvPath={common_base}/features/run322b_route_signal_forward_tier_a.csv",
            "InpFeatureCount=1",
            "InpFeatureCsvUseCommonFiles=true",
            "InpFeatureRequireTimestampMatch=true",
            "InpFeatureAllowLatestFallback=false",
            "InpFeatureStrictHeader=true",
            "InpCsvTimestampIsBarClose=true",
            f"InpFeatureOrderHash={feature_order.get('onnx_input_feature_order_hash', '')}",
            "InpFallbackEnabled=true",
            "InpFallbackTierLabel=Tier B partial-context fallback",
            f"InpFallbackFeatureCsvPath={common_base}/features/run322b_route_signal_forward_tier_b.csv",
            "InpFallbackFeatureCount=1",
            f"InpFallbackModelPath={onnx_recorded_path}",
            "InpFallbackModelId=cp322a_route_signal_identity_frozen_tier_b",
            "InpFallbackModelBackend=onnx",
            f"InpFallbackFeatureOrderHash={feature_order.get('onnx_input_feature_order_hash', '')}",
            "InpTelemetryEnabled=true",
            "InpTelemetryUseCommonFiles=true",
            f"InpTelemetryCsvPath={common_base}/telemetry/broker_current_day_forward_probe_telemetry.csv",
            f"InpSummaryCsvPath={common_base}/telemetry/broker_current_day_forward_probe_summary.csv",
            "InpShortThreshold=0.55",
            "InpLongThreshold=0.55",
            "InpMinMargin=0",
            "InpInvertSignal=false",
            "InpFallbackShortThreshold=0.55",
            "InpFallbackLongThreshold=0.55",
            "InpFallbackMinMargin=0",
            "InpFallbackInvertSignal=false",
            "InpAllowTrading=true",
            "InpFixedLot=0.42",
            "InpCloseOnFlatSignal=true",
            "InpReverseOnOppositeSignal=true",
            "InpCloseOnlyOnOppositeSignal=false",
            "InpMaxHoldBars=1",
            "InpMaxConcurrentPositions=1",
            "InpReentryCooldownBars=0",
            "InpSameDirectionReentryCooldownBars=0",
            "InpAtrSltpEnabled=true",
            "InpAtrPeriod=14",
            "InpAtrStopMultiplier=0.78",
            "InpAtrTakeProfitMultiplier=3.35",
            "InpAtrMinStopPoints=70",
            "InpAtrMaxStopPoints=900",
            "InpAtrMinTakeProfitPoints=100",
            "InpAtrMaxTakeProfitPoints=1800",
            "InpModelRiskSizingEnabled=true",
            "InpModelRiskMinPct=0.004",
            "InpModelRiskMaxPct=0.026",
            "InpModelRiskConfidenceFloor=0.58",
            "InpModelRiskConfidenceCeiling=0.99",
            "InpModelRiskFallbackLot=0.08",
            "InpExitRiskOverlayEnabled=false",
            "InpExitRiskCloseLongFeatureIndex=-1",
            "InpExitRiskCloseShortFeatureIndex=-1",
            "InpExitRiskCloseThreshold=0",
            "InpExitRiskMaxHoldFeatureIndex=-1",
            "InpExitRiskMinHoldBars=1",
            "InpEntryTransitionOnly=false",
            "InpMagic=1001010",
            "",
        ]
    )
    ini_text = "\n".join(
        [
            "[Tester]",
            "Expert=Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "Symbol=US100",
            "Period=M5",
            "Model=4",
            "Deposit=500",
            "Leverage=1:100",
            "Optimization=0",
            "ExecutionMode=0",
            "ForwardMode=0",
            "UseLocal=1",
            "UseRemote=0",
            "UseCloud=0",
            "ReplaceReport=1",
            "ShutdownTerminal=1",
            "FromDate=2026.04.14",
            "ToDate=2026.05.30",
            f"Report=Project_Obsidian_Prime_v2_{RUN_ID}_broker_current_day_forward_probe",
            "ExpertParameters=ObsidianPrimeV2_RuntimeProbeEA.set",
            "",
        ]
    )
    return [
        aw.write_text_lossless(TESTER_SET_TEMPLATE, set_text, False),
        aw.write_text_lossless(TESTER_INI_TEMPLATE, ini_text, False),
    ]


def build_route_signal_status(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    contract = src["stage328_contract"].get("contract", {})
    return [
        {
            "contract_id": f"{RUN_NUMBER}_route_signal_forward_handoff_status",
            "field_name": "run322b_route_signal_forward_tier_a_and_tier_b",
            "field_type": "two_csvs_required_before_actual_mt5",
            "required": "true",
            "source": aw.rel(STAGE328_SIGNAL_CONTRACT),
            "validation_rule": "must be generated from frozen contract without forward rank recalculation(고정 계약에서 생성, 전진 순위 재계산 금지)",
            "downstream_use": "InpFeatureCsvPath and InpFallbackFeatureCsvPath for cp322A identity ONNX(cp322A 정체성 ONNX 피처 CSV와 대체 피처 CSV)",
            "forbidden_inference": "split_rank_forward_generation_or_outcome_distillation(분할 순위 전진 생성 또는 결과 증류)",
            "effect": f"records Stage328 decision={src['stage328_contract'].get('decision')} and formula={contract.get('exact_formula')}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_contract_rows(kind: str) -> list[dict[str, Any]]:
    definitions = {
        "proxy": [
            ("bar_time", "datetime_utc", "proxy and MT5 telemetry", "exact timestamp join only", "row parity", "nearest timestamp join"),
            ("symbol", "string", "proxy and MT5 telemetry", "US100 only", "symbol parity", "cross-symbol comparison"),
            ("source", "enum_D_B_DB_none", "runtime handoff", "must be explicit or none", "D/B attribution", "source-free attribution"),
            ("direction", "enum_long_short_none", "decision output", "must be explicit", "long/short attribution", "direction-free parity"),
            ("proxy_expected_value", "float_or_signal", "frozen expected signal", "not null when proxy exists", "expected value", "proxy KPI authority"),
            ("mt5_runtime_probe_value", "float_or_signal", "MT5 telemetry", "not null after probe", "runtime probe value", "runtime authority claim"),
            ("difference", "float_or_exact_match", "harness computation", "tolerance stated", "mismatch audit", "silent mismatch"),
            ("usable_scope", "enum_signal_only_handoff_only_diagnostic", "review judgment", "not forward KPI", "proxy usability", "Forward Passed/Failed"),
            ("mismatch_reason", "string", "harness computation", "required if difference not exact", "repair memory", "unexplained mismatch"),
        ],
        "profit": [
            ("trade_id", "string", "MT5 report trade list", "unique", "trade count", "anonymous trade rows"),
            ("open_time", "datetime_utc", "MT5 report trade list", "open_time <= close_time", "session/hour/month", "timezone-free KPI"),
            ("close_time", "datetime_utc", "MT5 report trade list", "closed before KPI read", "equity curve", "floating-only profit"),
            ("direction", "enum_long_short", "MT5 report trade list", "long or short", "long/short attribution", "direction missing"),
            ("source", "enum_D_B_DB_none", "runtime telemetry", "explicit or none", "D/B attribution", "source-free KPI"),
            ("lot", "float", "MT5 report trade list", ">0", "lot normalized result", "lot optimization"),
            ("net_profit", "float", "MT5 report trade list", "cost included", "net/PF/expectancy", "gross-only profit"),
            ("balance_after", "float", "equity curve", "ordered by close time", "drawdown/recovery", "unordered curve"),
            ("equity_after", "float", "equity curve", "ordered if present", "underwater stretch", "unmarked missing equity"),
            ("spread_points", "float", "runtime telemetry", ">=0", "cost stress", "spread-free stress"),
            ("slippage_points", "float", "runtime telemetry", ">=0", "cost stress", "slippage-free stress"),
            ("chunk_id", "string", "curve harness", "predeclared chronological chunk", "worst chunk", "post-hoc chunk fit"),
            ("curve_pocket_id", "string", "curve harness", "predeclared pocket rule", "curve pocket", "curve cherry-pick"),
        ],
        "feature_last": [
            ("feature_last_timestamp", "datetime_utc", "feature package", "known before probe", "feature gap", "unknown feature boundary"),
            ("tester_last_observed_bar_time", "datetime_utc", "tester output", ">= feature_last for forward", "tester visibility", "stale tester history"),
            ("feature_last_reached", "bool", "harness computation", "true required before forward", "forward gate", "Forward claim while false"),
            ("tester_to_feature_last_gap_minutes", "float", "harness computation", "<=0 required before forward", "gap magnitude", "gap ignored"),
        ],
        "lookahead": [
            ("as_of_time", "datetime_utc", "harness clock", "required every row", "all gates", "implicit now"),
            ("bar_close_time", "datetime_utc", "broker bars", "<= as_of_time", "closed bar check", "open bar feature"),
            ("feature_time", "datetime_utc", "feature source", "<= decision_time", "feature boundary", "future feature"),
            ("label_time", "datetime_utc", "trade outcome", "> decision_time for labels only", "label boundary", "label in feature"),
            ("release_time", "datetime_utc_or_null", "macro sidecar", "<= as_of_time or null", "macro as-of", "future release join"),
            ("selection_time", "datetime_utc", "ledger", "before KPI read", "selection bias", "post-profit selection"),
            ("trade_index_target_used", "bool", "audit", "false", "trade-index guard", "trade index target"),
        ],
        "forensics": [
            ("terminal_path", "path", "local terminal", "exists before execution", "tester identity", "unknown terminal"),
            ("ea_entrypoint", "path_hash", "repo EA", "path and sha256", "EA identity", "anonymous EA"),
            ("set_file", "path_hash", "tester profile", "path and sha256", "parameter identity", "unknown parameters"),
            ("model_or_bundle_hash", "sha256", "ONNX/model manifest", "recorded", "model identity", "unhashed model"),
            ("deposit", "float", "tester settings", "recorded", "cost comparability", "unknown deposit"),
            ("leverage", "string", "tester settings", "recorded", "cost comparability", "unknown leverage"),
            ("modeling_mode", "string", "tester settings", "recorded", "cost comparability", "unknown model mode"),
            ("spread_commission_slippage", "string", "tester settings/telemetry", "recorded or missing named", "cost assumptions", "cost-free comparison"),
        ],
        "cost": [
            ("base", "stress_case", "trade list", "spread x1.0 slippage 0", "base metrics", "base omitted"),
            ("mild_spread", "stress_case", "trade list", "spread x1.25", "cost fragility", "spread stress omitted"),
            ("hard_spread", "stress_case", "trade list", "spread x1.50", "cost fragility", "spread stress omitted"),
            ("mild_slippage", "stress_case", "trade list", "1 point entry/exit", "slippage fragility", "slippage stress omitted"),
            ("hard_slippage", "stress_case", "trade list", "2 points entry/exit", "slippage fragility", "slippage stress omitted"),
            ("combined_hard", "stress_case", "trade list", "spread x1.50 and slippage 2", "combined stress", "combined stress omitted"),
        ],
        "lot": [
            ("lot", "float", "trade list", ">0", "lot normalization", "lot optimization"),
            ("contract_size", "float", "broker symbol spec", ">0 or missing named", "risk normalization", "unknown contract spec"),
            ("point_value", "float", "broker symbol spec", ">0 or missing named", "point PnL", "instrument mismatch"),
            ("net_per_lot", "float", "harness computation", "net_profit / lot", "expectancy per lot", "raw lot masked KPI"),
            ("dd_per_lot", "float", "harness computation", "drawdown / lot", "risk per lot", "drawdown masked by lot"),
        ],
        "regime": [
            ("direction", "enum_long_short", "trade list", "explicit", "direction attribution", "direction-free result"),
            ("session", "enum", "bar time", "as-of", "session slice", "session cherry-pick"),
            ("hour", "int_0_23", "bar time", "as-of", "hour slice", "hour cherry-pick"),
            ("month", "int_1_12", "bar time", "as-of", "month slice", "month cherry-pick"),
            ("volatility_bucket", "enum", "as-of features", "before decision", "volatility slice", "future volatility"),
            ("adx_bucket", "enum", "as-of features", "before decision", "ADX slice", "future ADX"),
            ("vix_bucket", "enum_missing_allowed", "as-of sidecar", "release_time <= as_of_time", "VIX slice", "future VIX"),
            ("usd_bucket", "enum_missing_allowed", "as-of sidecar", "release_time <= as_of_time", "USD slice", "future USD"),
            ("rate_regime", "enum_missing_allowed", "as-of sidecar", "known_at <= as_of_time", "rate regime", "future rate outcome"),
        ],
    }
    effects = {
        "proxy": "forces proxy expected value and MT5 runtime value comparison before use(사용 전 프록시 예상값과 MT5 런타임값 비교 강제)",
        "profit": "makes frozen forward MT5 KPI auditable from raw trades(원시 거래에서 고정 전진 MT5 KPI 감사 가능)",
        "feature_last": "blocks forward judgment until tester reaches feature_last(테스터가 feature_last에 도달할 때까지 전진 판정 차단)",
        "lookahead": "prevents look-ahead bias in runtime audit(런타임 감사의 미래참조 편향 방지)",
        "forensics": "prevents trusting tester output without identity(정체성 없는 테스터 출력 신뢰 방지)",
        "cost": "keeps cost stress attached to any profit read(모든 수익 판독에 비용 압박 연결)",
        "lot": "separates signal quality from lot sizing(신호 품질과 로트 크기 분리)",
        "regime": "keeps attribution as-of and not post-hoc(귀속을 시점 기준으로 유지)",
    }
    return [
        {
            "contract_id": f"{RUN_NUMBER}_{kind}_{name}",
            "field_name": name,
            "field_type": field_type,
            "required": "true",
            "source": source,
            "validation_rule": validation,
            "downstream_use": downstream,
            "forbidden_inference": forbidden,
            "effect": effects[kind],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, field_type, source, validation, downstream, forbidden in definitions[kind]
    ]


def build_checklist() -> list[dict[str, Any]]:
    return [
        {
            "step_id": f"{RUN_NUMBER}_step_01_identity_review",
            "sequence": "1",
            "action": "review frozen identity and route-signal boundary(고정 정체성과 경로 신호 경계 검토)",
            "required_input": aw.rel(FROZEN_SUBJECT_IDENTITY),
            "expected_output": "no model/threshold/D-B/risk/lot mutation(모델/임계값/D-B/위험/로트 변경 없음)",
            "pass_condition": "all frozen rows source_status not missing and route signal limitation named(고정 행 원천 존재와 경로 신호 한계 명명)",
            "fail_condition": "any hidden surface mutation or missing identity(숨은 표면 변경 또는 정체성 누락)",
            "effect": "protects cp322A freeze before runtime work(런타임 전 cp322A 고정 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "step_id": f"{RUN_NUMBER}_step_02_terminal_files",
            "sequence": "2",
            "action": "review terminal, EA, set, ini, and common-files paths(터미널/EA/set/ini/common files 경로 검토)",
            "required_input": aw.rel(RUNTIME_FILE_HANDOFF_MANIFEST),
            "expected_output": "all required handoff paths explicit(필수 인계 경로 명시)",
            "pass_condition": "terminal exists or review records exact blocker(터미널 존재 또는 정확한 차단 사유 기록)",
            "fail_condition": "anonymous or drifting tester path(익명 또는 흔들리는 테스터 경로)",
            "effect": "prevents runtime evidence drift(런타임 근거 드리프트 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "step_id": f"{RUN_NUMBER}_step_03_feature_last_gate",
            "sequence": "3",
            "action": "require feature_last reach before any forward decision(feature_last 도달 전 전진 판정 금지)",
            "required_input": aw.rel(FEATURE_LAST_GATE_CONTRACT),
            "expected_output": "feature_last_reached true after actual probe(실제 탐침 후 feature_last_reached true)",
            "pass_condition": "tester_last_observed_bar_time >= feature_last_timestamp(테스터 마지막 봉 >= 피처 마지막 시각)",
            "fail_condition": "tester_feature_last_gap_remains(테스터 feature_last 공백 지속)",
            "effect": "separates data visibility from strategy quality(데이터 가시성과 전략 품질 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "step_id": f"{RUN_NUMBER}_step_04_proxy_profit_outputs",
            "sequence": "4",
            "action": "require proxy-MT5 diff and raw trade KPI outputs(프록시-MT5 차이와 원시 거래 KPI 출력 요구)",
            "required_input": f"{aw.rel(PROXY_MT5_DIFF_OUTPUT_CONTRACT)};{aw.rel(PROFIT_TRADE_OUTPUT_CONTRACT)}",
            "expected_output": "row-level diff, net/PF/trades/DD/recovery/expectancy, curve pockets(행 단위 차이와 순익/PF/거래/DD/회복/기대값/곡선 포켓)",
            "pass_condition": "all required fields present and sorted by time(필수 필드 존재와 시간 정렬)",
            "fail_condition": "profit-only or proxy-only read(수익 단독 또는 프록시 단독 판독)",
            "effect": "keeps measurement complete before judgment(판정 전 측정 완전성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "step_id": f"{RUN_NUMBER}_step_05_forensics_and_stress",
            "sequence": "5",
            "action": "require tester forensics, lot normalization, cost stress, and regimes(테스터 포렌식/로트 정규화/비용 압박/국면 요구)",
            "required_input": f"{aw.rel(BACKTEST_FORENSICS_IDENTITY_CONTRACT)};{aw.rel(COST_STRESS_EXECUTION_CONTRACT)};{aw.rel(LOT_NORMALIZED_EXECUTION_CONTRACT)};{aw.rel(REGIME_ATTRIBUTION_EXECUTION_CONTRACT)}",
            "expected_output": "identity-bound KPI slices(정체성 묶인 KPI 조각)",
            "pass_condition": "tester identity and all stress/slice contracts reviewed(테스터 정체성과 압박/조각 계약 검토)",
            "fail_condition": "single headline KPI selection(단일 대표 KPI 선택)",
            "effect": "prevents overfit-friendly interpretation(과적합 친화 해석 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "step_id": f"{RUN_NUMBER}_step_06_no_lookahead",
            "sequence": "6",
            "action": "run no-lookahead runtime audit before any result claim(결과 주장 전 미래참조 방지 런타임 감사)",
            "required_input": aw.rel(NO_LOOKAHEAD_RUNTIME_AUDIT_CONTRACT),
            "expected_output": "as_of/bar_close/feature/label/release/selection audit(시점/봉마감/피처/라벨/발표/선택 감사)",
            "pass_condition": "no guard failure and no trade-index target(가드 실패 없음, 거래번호 타깃 없음)",
            "fail_condition": "future release or post-profit selection leak(미래 발표 또는 수익 후 선택 누수)",
            "effect": "keeps the previous look-ahead failure from returning(이전 미래참조 실패 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_handoff_manifest(manifest_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary = manifest_rows[0]
    return [
        {
            "handoff_id": f"{RUN_NUMBER}_set_template",
            "file_role": "tester set template(테스터 설정 템플릿)",
            "repo_template_path": aw.rel(TESTER_SET_TEMPLATE),
            "terminal_expected_path": (TESTER_PROFILE_ROOT / "ObsidianPrimeV2_RuntimeProbeEA.set").as_posix(),
            "common_files_expected_path": "not_applicable(해당 없음)",
            "required_before_runtime": "true",
            "required_after_runtime": "false",
            "validation_rule": "sha256 recorded before execution(실행 전 해시 기록)",
            "effect": "keeps parameter-only run variant explicit(파라미터 전용 실행 변형 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_id": f"{RUN_NUMBER}_ini_template",
            "file_role": "tester ini template(테스터 ini 템플릿)",
            "repo_template_path": aw.rel(TESTER_INI_TEMPLATE),
            "terminal_expected_path": (TESTER_PROFILE_ROOT / TESTER_INI_TEMPLATE.name).as_posix(),
            "common_files_expected_path": "not_applicable(해당 없음)",
            "required_before_runtime": "true",
            "required_after_runtime": "false",
            "validation_rule": "FromDate/ToDate/report/profile reviewed(시작일/종료일/보고/profile 검토)",
            "effect": "keeps Strategy Tester settings explicit(전략 테스터 설정 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_id": f"{RUN_NUMBER}_feature_csv",
            "file_role": "forward route-signal feature csv pair(전진 경로 신호 피처 CSV 쌍)",
            "repo_template_path": aw.rel(ROUTE_SIGNAL_HANDOFF_STATUS),
            "terminal_expected_path": "not_applicable(해당 없음)",
            "common_files_expected_path": f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}/broker_current_day_forward_probe/features/run322b_route_signal_forward_tier_a.csv;Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}/broker_current_day_forward_probe/features/run322b_route_signal_forward_tier_b.csv",
            "required_before_runtime": "true",
            "required_after_runtime": "false",
            "validation_rule": "must exist before actual cp322A forward run(실제 cp322A 전진 실행 전 존재 필수)",
            "effect": "blocks fake forward execution without run322b_route_signal(경로 신호 없는 가짜 전진 실행 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_id": f"{RUN_NUMBER}_telemetry_summary",
            "file_role": "runtime telemetry and summary(런타임 기록과 요약)",
            "repo_template_path": aw.rel(MT5_PROBE_EXECUTION_MANIFEST),
            "terminal_expected_path": "not_applicable(해당 없음)",
            "common_files_expected_path": f"{primary['expected_telemetry_path']};{primary['expected_summary_path']}",
            "required_before_runtime": "false",
            "required_after_runtime": "true",
            "validation_rule": "files exist, non-empty, feature_ready/model_ok checked(파일 존재/비어있지 않음/피처 준비/모델 정상 확인)",
            "effect": "turns MT5 run into comparable runtime evidence(MT5 실행을 비교 가능한 런타임 근거로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "handoff_id": f"{RUN_NUMBER}_tester_report",
            "file_role": "Strategy Tester report(전략 테스터 보고서)",
            "repo_template_path": aw.rel(MT5_PROBE_EXECUTION_MANIFEST),
            "terminal_expected_path": aw.rel(MT5_DIR / "reports"),
            "common_files_expected_path": "not_applicable(해당 없음)",
            "required_before_runtime": "false",
            "required_after_runtime": "true",
            "validation_rule": "report parsed with tester identity(테스터 정체성과 함께 보고서 파싱)",
            "effect": "keeps trade KPI tied to report identity(거래 KPI를 보고서 정체성에 묶음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BL_review_mt5_probe_execution_package",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "MT5 probe execution package review(MT5 탐침 실행 패키지 검토)",
            "inputs_to_review": ";".join(aw.rel(path) for path in OUTPUT_FILES if path not in (FINAL_DECISION, RUN_MANIFEST)),
            "must_confirm": "frozen identity, route-signal handoff status, tester identity, feature_last gate, proxy-MT5 diff, trade KPI, cost stress, lot-normalization, regimes, no-lookahead(고정 정체성/경로 신호 인계 상태/테스터 정체성/feature_last 게이트/프록시-MT5 차이/거래 KPI/비용 압박/로트 정규화/국면/미래참조 방지)",
            "must_reject_if": "any model training, threshold retune, D/B rewrite, lot optimization, fake forward signal, proxy KPI authority, Forward/Runtime/Goal claim(모델 학습/임계값 재조정/D-B 재작성/로트 최적화/가짜 전진 신호/프록시 KPI 권위/전진-런타임-목표 주장)",
            "expected_outputs": "review decision: actual MT5 attempt allowed or exact repair/block reason(검토 결정: 실제 MT5 시도 허용 또는 정확한 수리/차단 사유)",
            "priority": "P0",
            "effect": "forces review before any external MT5 execution(외부 MT5 실행 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def count_passed(rows: Sequence[Mapping[str, str]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def build_gates(
    src: Mapping[str, Any],
    identity_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    checklist_rows: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    profit_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
    lookahead_rows: Sequence[Mapping[str, Any]],
    forensics_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    lot_rows: Sequence[Mapping[str, Any]],
    regime_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent = src["parent_final"]
    source_gates_passed = count_passed(src["parent_gates"])
    feature_order_hash = str(src["feature_order"].get("onnx_input_feature_order_hash", ""))
    readiness_values = {str(row.get("execution_readiness_status", "")) for row in manifest_rows}
    gate_specs = [
        ("bk_gate_parent_loaded", parent.get("next_action") == RUN_ID, f"parent_next={parent.get('next_action')}", "run337BJ opens run337BK(337BJ가 337BK를 엶)"),
        ("bk_gate_parent_gates_passed", parent.get("passed_gates") == parent.get("gate_rows") == 14 and source_gates_passed == 14, f"parent_gates={parent.get('passed_gates')}/{parent.get('gate_rows')};audit={source_gates_passed}/14", "run337BJ all gates passed(337BJ 모든 게이트 통과)"),
        ("bk_gate_frozen_identity_complete", len(identity_rows) == 7 and all(row.get("must_preserve") == "true" for row in identity_rows), f"identity_rows={len(identity_rows)}", "all frozen identity rows materialized(모든 고정 정체성 행 물질화)"),
        ("bk_gate_manifest_complete", len(manifest_rows) == 3 and all(row.get("feature_order_hash") == feature_order_hash for row in manifest_rows), f"manifest_rows={len(manifest_rows)};feature_order_hash={feature_order_hash}", "three probe roles with same feature order hash(세 탐침 역할과 같은 피처 순서 해시)"),
        ("bk_gate_route_signal_boundary_named", len(route_rows) == 1 and "split_rank" in route_rows[0].get("forbidden_inference", ""), f"route_contract={len(route_rows)}", "route signal handoff limitation named(경로 신호 인계 한계 명명)"),
        ("bk_gate_no_fake_execution_readiness", "blocked_until_run322b_route_signal_forward_handoff_exists" in readiness_values, f"readiness={sorted(readiness_values)}", "primary actual MT5 is blocked until handoff exists(주 실제 MT5는 인계 전 차단)"),
        ("bk_gate_checklist_ordered", [row["sequence"] for row in checklist_rows] == ["1", "2", "3", "4", "5", "6"], f"steps={','.join(row['sequence'] for row in checklist_rows)}", "ordered checklist exists(순서 있는 체크리스트 존재)"),
        ("bk_gate_handoff_paths_complete", len(handoff_rows) == 5 and all(row.get("validation_rule") for row in handoff_rows), f"handoff_rows={len(handoff_rows)}", "handoff file paths are explicit(인계 파일 경로 명시)"),
        ("bk_gate_proxy_profit_contracts_complete", len(proxy_rows) >= 8 and len(profit_rows) >= 11, f"proxy={len(proxy_rows)};profit={len(profit_rows)}", "proxy and profit output contracts complete(프록시와 수익 출력 계약 완성)"),
        ("bk_gate_feature_last_and_lookahead_contracts", len(feature_rows) >= 4 and len(lookahead_rows) >= 7, f"feature={len(feature_rows)};lookahead={len(lookahead_rows)}", "feature_last and no-lookahead contracts complete(feature_last와 미래참조 방지 계약 완성)"),
        ("bk_gate_forensics_cost_lot_regime_contracts", len(forensics_rows) >= 8 and len(cost_rows) >= 6 and len(lot_rows) >= 5 and len(regime_rows) >= 8, f"forensics={len(forensics_rows)};cost={len(cost_rows)};lot={len(lot_rows)};regime={len(regime_rows)}", "forensics/cost/lot/regime contracts complete(포렌식/비용/로트/국면 계약 완성)"),
        ("bk_gate_templates_written", aw.path_exists(TESTER_SET_TEMPLATE) and aw.path_exists(TESTER_INI_TEMPLATE), f"set={path_status(TESTER_SET_TEMPLATE)};ini={path_status(TESTER_INI_TEMPLATE)}", "tester templates written(테스터 템플릿 작성됨)"),
        ("bk_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue={len(queue_rows)};next={queue_rows[0].get('next_run_id') if queue_rows else 'missing'}", "run337BL review queue ready(337BL 검토 대기열 준비)"),
        ("bk_gate_no_forbidden_claims", True, "forward=not_claimed;runtime=not_claimed;goal=not_claimed;mt5_execution=not_run", "no Forward/Runtime/Goal or MT5 execution claim(전진/런타임/목표 또는 MT5 실행 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "blocks actual MT5 execution unless package identity and no-lookahead gates are reviewed(패키지 정체성과 미래참조 방지 게이트 검토 전 실제 MT5 실행 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in gate_specs
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            REFERENCE_SCOUT_RECEIPT,
            {
                "skill": "obsidian-reference-scout",
                "run_id": RUN_ID,
                "question": "MT5 file handoff and Strategy Tester package boundaries(MT5 파일 인계와 전략 테스터 패키지 경계)",
                "sources_checked": [
                    "https://www.mql5.com/en/docs/files",
                    "https://www.mql5.com/en/docs/runtime/testing",
                    "https://www.mql5.com/en/docs/basis/variables/inputvariables",
                ],
                "source_quality": "official_docs(공식 문서)",
                "found_pattern": "MQL5 file work is sandboxed to terminal MQL5/Files or Common/Files, and Strategy Tester output must be tied to tester identity(MQL5 파일은 터미널 MQL5/Files 또는 Common/Files 샌드박스에 묶이고, 전략 테스터 출력은 테스터 정체성과 묶어야 함)",
                "project_fit": "package records common-files paths, tester profile paths, .set, .ini, EA, and module hashes(패키지가 common files 경로/테스터 profile 경로/.set/.ini/EA/모듈 해시 기록)",
                "do_not_copy": "no external code copied(외부 코드 복사 없음)",
                "recommended_use": "adapt for path and identity checklist(경로와 정체성 체크리스트에 맞춰 적용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUN_EVIDENCE_RECEIPT,
            {
                "skill": "obsidian-run-evidence-system",
                "run_id": RUN_ID,
                "measurement_scope": "runtime_probe package only; no MT5 KPI yet(런타임 탐침 패키지 전용, 아직 MT5 KPI 없음)",
                "management_state": "run folder, manifest, report, registry rows materialized(실행 폴더/목록/보고/등록부 행 물질화)",
                "judgment_class": "inconclusive_for_forward_by_design(설계상 전진 판정 불충분)",
                "scoreboard": "runtime_parity",
                "parity_level": "P0_unverified",
                "wfo_status": "not_applicable",
                "registry_update_required": "yes",
                "negative_memory_required": "no",
                "hard_gate_applicable": "no",
                "evidence_boundary": "probe_package_not_runtime_authority(탐침 패키지, 런타임 권위 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            BACKTEST_FORENSICS_RECEIPT,
            {
                "skill": "obsidian-backtest-forensics",
                "run_id": RUN_ID,
                "tester_identity": "US100 M5, model 4 real ticks, deposit 500, leverage 1:100, portable terminal path recorded(US100 5분봉/model 4 실제 틱/예치금 500/레버리지 1:100/휴대용 터미널 경로 기록)",
                "ea_identity": f"entrypoint={aw.rel(EA_ENTRYPOINT)};modules={include_module_hashes()}",
                "report_identity": "expected report paths recorded; no report produced in run337BK(예상 보고서 경로 기록, run337BK에서 보고서 생성 없음)",
                "trade_evidence": "missing until actual MT5 probe(실제 MT5 탐침 전 누락)",
                "cost_assumptions": "spread/slippage/commission contract recorded, no stress result yet(스프레드/슬리피지/커미션 계약 기록, 아직 압박 결과 없음)",
                "forensic_checks": [aw.rel(BACKTEST_FORENSICS_IDENTITY_CONTRACT), aw.rel(TESTER_COMMAND_CHECKLIST)],
                "backtest_judgment": "inconclusive_package_only(패키지 전용 불충분)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "skill": "obsidian-runtime-parity",
                "run_id": RUN_ID,
                "research_path": aw.rel(Path(__file__)),
                "runtime_path": aw.rel(EA_ENTRYPOINT),
                "shared_contract": "cp322A feature order, ONNX identity surface, route signal CSV, telemetry diff(cp322A 피처 순서/ONNX 정체성 표면/경로 신호 CSV/기록 차이)",
                "known_differences": "actual MT5 runtime output not produced; route signal forward handoff still required(실제 MT5 런타임 출력 미생성, 전진 경로 신호 인계 필요)",
                "parity_check": "package contract only, no runtime authority(패키지 계약 전용, 런타임 권위 없음)",
                "parity_identity": f"parent={PARENT_RUN_ID};package={RUN_ID}",
                "runtime_claim_boundary": "research_only_no_runtime_authority(연구 전용, 런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "skill": "obsidian-data-integrity",
                "run_id": RUN_ID,
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "UTC feature_last and tester bar close are contract fields(UTC feature_last와 테스터 봉 마감이 계약 필드)",
                "sample_scope": "post-OOS forward package after 2026-04-14, no new KPI sample yet(2026-04-14 이후 전진 패키지, 아직 새 KPI 표본 없음)",
                "missing_or_duplicate_check": "required in run337BL/actual probe review(run337BL/실제 탐침 검토에서 필수)",
                "feature_label_boundary": "route signal forward CSV cannot be generated by forward rank recalculation(전진 경로 신호 CSV는 전진 순위 재계산으로 생성 금지)",
                "split_boundary": "frozen cp322A artifact and forward holdout separated(고정 cp322A 산출물과 전진 보류 분리)",
                "leakage_risk": "split-rank forward generation and trade-index target(분할 순위 전진 생성과 거래번호 타깃)",
                "data_hash_or_identity": f"artifact_registry_run={RUN_ID}",
                "integrity_judgment": "usable_with_boundary_for_package_review(패키지 검토에 경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "skill": "obsidian-performance-attribution",
                "run_id": RUN_ID,
                "observed_change": "no trading KPI changed; package makes future attribution required(거래 KPI 변화 없음, 패키지가 향후 귀속을 필수화)",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "not_applicable_until_actual_trade_list(실제 거래 목록 전 해당 없음)",
                "segment_checks": "direction/session/hour/month/volatility/ADX/VIX/USD/rate contracts materialized(방향/세션/시간/월/변동성/ADX/VIX/USD/금리 계약 물질화)",
                "trade_shape": "contract-only(계약 전용)",
                "alternative_explanations": "tester feature gap or route signal handoff may block actual run(테스터 피처 공백 또는 경로 신호 인계가 실제 실행 차단 가능)",
                "attribution_confidence": "inconclusive",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "skill": "obsidian-artifact-lineage",
                "run_id": RUN_ID,
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "availability": "tracked_and_reproducible_from_script(추적되고 스크립트로 재현 가능)",
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "skill": "obsidian-result-judgment",
                "run_id": RUN_ID,
                "result_subject": "MT5 probe execution package(MT5 탐침 실행 패키지)",
                "evidence_available": [aw.rel(path) for path in OUTPUT_FILES],
                "evidence_missing": "actual MT5 tester output, trade list, computed forward KPI, feature_last pass(실제 MT5 테스터 출력/거래 목록/계산 전진 KPI/feature_last 통과)",
                "judgment_label": "exploratory_package_completed(탐색 패키지 완료)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 실제 MT5 결과가 아니라 실행 패키지다.",
            },
        ),
        (
            ENVIRONMENT_RECEIPT,
            {
                "skill": "obsidian-environment-reproducibility",
                "run_id": RUN_ID,
                "execution_environment": "Windows, PowerShell, local portable MT5 path recorded(윈도우/파워셸/로컬 휴대용 MT5 경로 기록)",
                "dependency_surface": "standard library only for package generation(패키지 생성은 표준 라이브러리만 사용)",
                "entry_command": f"python {aw.rel(Path(__file__))}",
                "local_assumptions": [TERMINAL_PATH.as_posix(), COMMON_FILES_ROOT.as_posix()],
                "clean_checkout_status": "reproducible_with_local_mt5_setup(로컬 MT5 설정 포함 재현 가능)",
                "recovery_instruction": "review paths and create missing route-signal handoff before actual MT5(경로 검토 후 실제 MT5 전 누락 경로 신호 인계 생성)",
                "reproducibility_judgment": "local_only_for_mt5_but_repo_package_reproducible(MT5는 로컬 전용, 저장소 패키지는 재현 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            CLAIM_DISCIPLINE_RECEIPT,
            {
                "skill": "obsidian-claim-discipline",
                "run_id": RUN_ID,
                "claim_guard": "Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, Goal Achieve all not claimed(전진 통과/실패, 실거래 준비, 배포, 운영 승격, 런타임 권위, 목표 달성 모두 주장 안 함)",
                "pending_terms": "actual MT5 output pending; route signal handoff pending(실제 MT5 출력 대기, 경로 신호 인계 대기)",
                "downgraded_scope": "package materialization only(패키지 물질화 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BK MT5 Probe Package(MT5 탐침 패키지)

## Conclusion(결론)

run337BK(337BK 실행)는 cp322A(322A 후보)를 고정한 상태에서 MT5 probe execution package(MT5 탐침 실행 패키지)를 만들었다.

Effect(효과): 실제 Strategy Tester output(전략 테스터 출력)을 만들지는 않았고, run337BL(337BL 실행)이 실행 허용 여부를 검토할 수 있게 tester identity(테스터 정체성), route-signal handoff(경로 신호 인계), feature_last gate(feature_last 게이트), proxy-MT5 diff(프록시-MT5 차이), profit/cost/lot/regime contracts(수익/비용/로트/국면 계약)를 묶었다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- package_rows(패키지 행): `{final['manifest_rows']}`
- identity_rows(정체성 행): `{final['identity_rows']}`
- checklist_steps(체크리스트 단계): `{final['checklist_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Important Boundary(중요 경계)

- actual MT5 execution(실제 MT5 실행): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- route signal handoff(경로 신호 인계): `required_before_actual_cp322A_forward_run`

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BK MT5 Probe Package(결정: 337단계 337BK MT5 탐침 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): package review(패키지 검토)로 넘어가되, 실제 MT5 execution(실제 MT5 실행), forward decision(전진 판정), runtime authority(런타임 권위)는 아직 열지 않는다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bj.bi.bh.bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BK focus")
    workspace = bj.bi.bh.bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BK focus complete: run337BK(337BK 실행)은 `{final['status']}`로 "
        f"MT5 probe execution package(MT5 탐침 실행 패키지)를 물질화했다. Effect(효과): "
        f"package rows(패키지 행) `{final['manifest_rows']}`, gates(게이트) "
        f"`{final['passed_gates']}/{final['gate_rows']}`이며 실제 MT5/Forward/Goal(실제 MT5/전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bj.bi.bh.bg.remove_markdown_section(current_text, "## Stage337 run337BK(337BK 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bj.bi.bh.bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BK(337BK 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BK(337BK 실행)는 MT5 probe execution package(MT5 탐침 실행 패키지)를 만들었고 run337BL(337BL 실행) 검토를 연다. 실제 MT5/Forward/Goal(실제 MT5/전진/목표)은 주장하지 않는다.

"""
    marker = "## Stage337 run337BJ"
    current = current.replace(marker, entry + marker, 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- mt5_probe_package_rows(MT5 탐침 패키지 행): `{final['manifest_rows']}`
- frozen_identity_rows(고정 정체성 행): `{final['identity_rows']}`
- command_checklist_rows(명령 체크리스트 행): `{final['checklist_rows']}`
- route_signal_handoff(경로 신호 인계): `required_before_actual_cp322A_forward_run`
- actual_mt5_execution(실제 MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_run337BL_review_pending`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BK(337BK 실행)는 실행 전 패키지만 만들었고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief_text, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_text = bj.bi.bh.bg.remove_lines_containing(brief_text, "run337BK(337BK 실행):")
    brief_line = (
        f"\n- run337BK(337BK 실행): `{final['status']}`. Effect(효과): MT5 probe execution package(MT5 탐침 실행 패키지)를 "
        f"물질화하고 run337BL(337BL 실행) 검토를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief_text.rstrip() + brief_line, brief_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = bj.bi.bh.bg.remove_lines_containing(changelog_text, f",{RUN_ID},")
    changelog_line = f"{TODAY},Stage337,{RUN_ID},{final['status']},{final['judgment']},{aw.rel(REPORT_PATH)}\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_line, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_probe_execution_package_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};actual_mt5_not_run;goal_achieve_not_claimed.",
        "work_family": "runtime_backtest",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_probe_package",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BK MT5 probe execution package",
        "tier_scope": "research_package_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "runtime_backtest",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"package_rows={final['manifest_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;actual_mt5_not_run;route_signal_handoff_required;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_package_only(주장 범위 밖, 패키지 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_probe_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_backtest",
        "evidence_scope": "run337BJ reviewed harness and cp322A frozen identity",
        "kpi_scope": "package_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;actual_mt5_not_run;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_probe_package",
        "family": "mt5_probe_execution_package_without_db",
        "question": "can a cp322A-frozen MT5 probe package be materialized without surface mutation",
        "metric_scope": "runtime_identity_feature_last_proxy_profit_cost_lot_regime_no_lookahead",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(MT5_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()

    template_paths = build_tester_templates(src)
    identity_rows = build_frozen_identity(src)
    identity_path = aw.write_csv(FROZEN_SUBJECT_IDENTITY, IDENTITY_COLUMNS, identity_rows)
    manifest_rows = build_probe_manifest(src)
    manifest_csv_path = aw.write_csv(MT5_PROBE_EXECUTION_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    checklist_rows = build_checklist()
    checklist_path = aw.write_csv(TESTER_COMMAND_CHECKLIST, CHECKLIST_COLUMNS, checklist_rows)
    handoff_rows = build_handoff_manifest(manifest_rows)
    handoff_path = aw.write_csv(RUNTIME_FILE_HANDOFF_MANIFEST, HANDOFF_COLUMNS, handoff_rows)
    proxy_rows = build_contract_rows("proxy")
    proxy_path = aw.write_csv(PROXY_MT5_DIFF_OUTPUT_CONTRACT, CONTRACT_COLUMNS, proxy_rows)
    profit_rows = build_contract_rows("profit")
    profit_path = aw.write_csv(PROFIT_TRADE_OUTPUT_CONTRACT, CONTRACT_COLUMNS, profit_rows)
    feature_rows = build_contract_rows("feature_last")
    feature_path = aw.write_csv(FEATURE_LAST_GATE_CONTRACT, CONTRACT_COLUMNS, feature_rows)
    lookahead_rows = build_contract_rows("lookahead")
    lookahead_path = aw.write_csv(NO_LOOKAHEAD_RUNTIME_AUDIT_CONTRACT, CONTRACT_COLUMNS, lookahead_rows)
    forensics_rows = build_contract_rows("forensics")
    forensics_path = aw.write_csv(BACKTEST_FORENSICS_IDENTITY_CONTRACT, CONTRACT_COLUMNS, forensics_rows)
    cost_rows = build_contract_rows("cost")
    cost_path = aw.write_csv(COST_STRESS_EXECUTION_CONTRACT, CONTRACT_COLUMNS, cost_rows)
    lot_rows = build_contract_rows("lot")
    lot_path = aw.write_csv(LOT_NORMALIZED_EXECUTION_CONTRACT, CONTRACT_COLUMNS, lot_rows)
    regime_rows = build_contract_rows("regime")
    regime_path = aw.write_csv(REGIME_ATTRIBUTION_EXECUTION_CONTRACT, CONTRACT_COLUMNS, regime_rows)
    route_rows = build_route_signal_status(src)
    route_path = aw.write_csv(ROUTE_SIGNAL_HANDOFF_STATUS, CONTRACT_COLUMNS, route_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BL_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(
        src,
        identity_rows,
        manifest_rows,
        checklist_rows,
        handoff_rows,
        proxy_rows,
        profit_rows,
        feature_rows,
        lookahead_rows,
        forensics_rows,
        cost_rows,
        lot_rows,
        regime_rows,
        route_rows,
        queue_rows,
    )
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BK_mt5_probe_package_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "mt5_probe_package_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BK_mt5_probe_package_before_review",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BK_mt5_probe_package_gate_failure_v1",
        "manifest_rows": len(manifest_rows),
        "identity_rows": len(identity_rows),
        "checklist_rows": len(checklist_rows),
        "handoff_rows": len(handoff_rows),
        "proxy_contract_rows": len(proxy_rows),
        "profit_contract_rows": len(profit_rows),
        "feature_last_contract_rows": len(feature_rows),
        "lookahead_contract_rows": len(lookahead_rows),
        "forensics_contract_rows": len(forensics_rows),
        "cost_contract_rows": len(cost_rows),
        "lot_contract_rows": len(lot_rows),
        "regime_contract_rows": len(regime_rows),
        "route_signal_contract_rows": len(route_rows),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "actual_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(Path(__file__)),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "run_variant_boundary": "entrypoint unchanged + parameter template only(진입점 유지 + 파라미터 템플릿만)",
        "external_verification_status": "out_of_scope_by_claim_package_only(주장 범위 밖, 패키지 전용)",
        "actual_mt5_execution": "not_run",
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "forward rank recalculation(전진 순위 재계산)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "runtime authority claim(런타임 권위 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        *template_paths,
        identity_path,
        manifest_csv_path,
        checklist_path,
        handoff_path,
        proxy_path,
        profit_path,
        feature_path,
        lookahead_path,
        forensics_path,
        cost_path,
        lot_path,
        regime_path,
        route_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "manifest_rows": final["manifest_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "actual_mt5_execution": final["actual_mt5_execution"],
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
