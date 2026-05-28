from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_proxy_survivor_row_level_runtime_probe_inputs as eh  # noqa: E402
from stage_pipelines.stage337 import review_proxy_survivor_runtime_probe_inputs as ei  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = eh.STAGE_ID
RUN_NUMBER = "run337EJ"
RUN_ID = "run337EJ_materialize_argmax_adapter_parity_probe_contract_without_db_v1"
PARENT_RUN_ID = ei.RUN_ID
NEXT_RUN_ID = "run337EK_implement_argmax_probe_decision_surface_without_db_v1"
STATUS = "completed_stage337EJ_argmax_adapter_parity_contract_materialized_no_mt5_no_selection"
JUDGMENT = "argmax_probe_contract_materialized_but_mqh_adapter_not_implemented_no_runtime_authority"
DECISION = "stage337EJ_open_run337EK_implement_argmax_probe_decision_surface"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EJ_argmax_adapter_parity_contract_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EJ_argmax_adapter_parity_contract_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EJ_argmax_adapter_parity_contract.md"
SELECTED_STATUS = eh.SELECTED_STATUS
STAGE_BRIEF = eh.STAGE_BRIEF
WORKSPACE_STATE = eh.WORKSPACE_STATE
CURRENT_STATE = eh.CURRENT_STATE
CHANGELOG = eh.CHANGELOG
RUN_REGISTRY = eh.RUN_REGISTRY
ALPHA_LEDGER = eh.ALPHA_LEDGER
ARTIFACT_REGISTRY = eh.ARTIFACT_REGISTRY
STAGE_LEDGER = eh.STAGE_LEDGER

EI_FINAL = ei.FINAL_DECISION
EI_GATES = ei.REQUIRED_GATE_AUDIT
EI_ADAPTER_REVIEW = ei.ADAPTER_REVIEW
EI_FEATURE_REVIEW = ei.FEATURE_REVIEW
EI_ATTEMPT_DECISION = ei.ATTEMPT_DECISION
EI_EJ_QUEUE = ei.EJ_QUEUE
EH_RUNTIME_MANIFEST = eh.RUNTIME_MANIFEST
EH_FEATURE_HANDOFF = eh.FEATURE_HANDOFF
EH_PROXY_EXPECTED = eh.PROXY_EXPECTED
EH_WATCH_POLICY = eh.WATCH_POLICY

MODEL_RUNTIME = ei.MODEL_RUNTIME
DECISION_SURFACE = ei.DECISION_SURFACE
RUNTIME_EA = ei.RUNTIME_EA
MT5_OUTPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

ARGMAX_CONTRACT = RUN_DIR / "argmax_decision_surface_contract.csv"
ADAPTER_PROBE_MANIFEST = RUN_DIR / "adapter_parity_probe_manifest.csv"
FEATURE_HANDOFF_CONTRACT = RUN_DIR / "feature_common_files_handoff_contract.csv"
PROBABILITY_OUTPUT_AUDIT = RUN_DIR / "probability_output_contract_audit.csv"
IMPLEMENTATION_QUEUE = RUN_DIR / "run337EK_argmax_probe_implementation_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EI_FINAL,
    EI_GATES,
    EI_ADAPTER_REVIEW,
    EI_FEATURE_REVIEW,
    EI_ATTEMPT_DECISION,
    EI_EJ_QUEUE,
    EH_RUNTIME_MANIFEST,
    EH_FEATURE_HANDOFF,
    EH_PROXY_EXPECTED,
    EH_WATCH_POLICY,
    MODEL_RUNTIME,
    DECISION_SURFACE,
    RUNTIME_EA,
    MT5_OUTPUT_CONTRACT,
)
OUTPUT_FILES = (
    ARGMAX_CONTRACT,
    ADAPTER_PROBE_MANIFEST,
    FEATURE_HANDOFF_CONTRACT,
    PROBABILITY_OUTPUT_AUDIT,
    IMPLEMENTATION_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
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

CONTRACT_COLUMNS = (
    "contract_key",
    "required_value",
    "source_evidence",
    "parity_status",
    "enforcement_target",
    "next_condition",
    "effect",
    "claim_boundary",
)
PROBE_COLUMNS = (
    "probe_id",
    "model_id",
    "proxy_rank",
    "onnx_path",
    "onnx_sha256",
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "output_contract_id",
    "decision_mode_required",
    "ea_required_change",
    "mt5_execution_allowed_now",
    "expected_compare_keys",
    "source_expected_contract",
    "watch_policy",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "included_features_sha256",
    "source_model_input",
    "common_files_target",
    "strict_header_required",
    "timestamp_policy",
    "materialization_status",
    "effect",
    "claim_boundary",
)
AUDIT_COLUMNS = (
    "audit_id",
    "source_path",
    "observed",
    "required_for_argmax_probe",
    "status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "passed", "active"}


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def file_contains(path: Path, pattern: str) -> bool:
    return pattern in io_path(path).read_text(encoding="utf-8-sig")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_argmax_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_key": "output_probability_order",
            "required_value": "[p_short,p_flat,p_long]",
            "source_evidence": f"{rel(MT5_OUTPUT_CONTRACT)};{rel(MODEL_RUNTIME)};{rel(EH_RUNTIME_MANIFEST)}",
            "parity_status": "materialized_contract",
            "enforcement_target": "ModelRuntime output unpacking and telemetry",
            "next_condition": "compile adapter and compare runtime probability tape",
            "effect": "locks probability meaning before any MT5 run(확률 의미를 MT5 실행 전에 고정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "class_order",
            "required_value": "0=short;1=flat;2=long",
            "source_evidence": f"{rel(EH_RUNTIME_MANIFEST)} class_order_json",
            "parity_status": "materialized_contract",
            "enforcement_target": "decision surface and runtime telemetry",
            "next_condition": "runtime output must emit the same labels",
            "effect": "keeps Python and EA labels aligned(Python과 EA 라벨을 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "decision_rule",
            "required_value": "argmax over all three probabilities",
            "source_evidence": f"{rel(EH_RUNTIME_MANIFEST)} decision_policy",
            "parity_status": "materialized_contract",
            "enforcement_target": "new explicit probe mode only",
            "next_condition": "add non-default argmax probe mode and static review",
            "effect": "matches proxy replay without threshold retuning(임계값 조정 없이 프록시 재생과 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "tie_rule",
            "required_value": "first maximum wins in [short,flat,long] order",
            "source_evidence": "numpy argmax replay convention(넘파이 argmax 재생 관례)",
            "parity_status": "materialized_contract_watch_required",
            "enforcement_target": "argmax probe helper",
            "next_condition": "runtime diff summary must report exact tie count",
            "effect": "prevents silent tie-policy drift(동률 규칙 드리프트 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "invalid_probability_rule",
            "required_value": "flat with probability_invalid reason",
            "source_evidence": f"{rel(DECISION_SURFACE)} finite probability guard",
            "parity_status": "materialized_contract",
            "enforcement_target": "argmax probe helper",
            "next_condition": "compile and skip/flat telemetry review",
            "effect": "keeps runtime fail-safe behavior(런타임 안전 동작 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "threshold_policy",
            "required_value": "not applicable for argmax parity probe; no threshold sweep",
            "source_evidence": f"{rel(EH_RUNTIME_MANIFEST)} threshold_policy",
            "parity_status": "materialized_contract",
            "enforcement_target": "probe settings",
            "next_condition": "new probe mode must not alter default thresholds",
            "effect": "blocks hidden threshold tuning(숨은 임계값 튜닝 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "default_surface_preservation",
            "required_value": "current threshold/margin default remains available",
            "source_evidence": f"{rel(MT5_OUTPUT_CONTRACT)} section 14.3;{rel(DECISION_SURFACE)}",
            "parity_status": "materialized_contract",
            "enforcement_target": "MQL implementation",
            "next_condition": "implementation diff must show explicit mode switch",
            "effect": "prevents global behavior replacement(전체 동작 교체 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "parity_probe_execution_policy",
            "required_value": "telemetry/probability tape first; trading authority remains closed",
            "source_evidence": f"{rel(EI_ATTEMPT_DECISION)}",
            "parity_status": "materialized_contract",
            "enforcement_target": "runtime probe setup",
            "next_condition": "runtime probability tape and diff summary exist",
            "effect": "separates parity from trading claims(동등성과 거래 주장을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_key": "feature_order_policy",
            "required_value": "use EH feature_order_hash exactly; no feature add/reorder",
            "source_evidence": f"{rel(EH_FEATURE_HANDOFF)};{rel(EI_FEATURE_REVIEW)}",
            "parity_status": "materialized_contract",
            "enforcement_target": "Common Files handoff and EA strict header",
            "next_condition": "feature CSV materialization hash matches contract",
            "effect": "blocks hidden feature drift(숨은 피처 드리프트 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_adapter_probe_manifest() -> list[dict[str, Any]]:
    runtime = pd.read_csv(io_path(EH_RUNTIME_MANIFEST))
    rows: list[dict[str, Any]] = []
    for row in runtime.to_dict("records"):
        rows.append(
            {
                "probe_id": row["probe_id"],
                "model_id": row["model_id"],
                "proxy_rank": int(row["proxy_rank"]),
                "onnx_path": row["onnx_path"],
                "onnx_sha256": row["onnx_sha256"],
                "feature_set_id": row["feature_set_id"],
                "feature_count": int(row["feature_count"]),
                "feature_order_hash": row["feature_order_hash"],
                "output_contract_id": "stage337EJ_argmax_probe_output_contract_v1",
                "decision_mode_required": "argmax_probe_non_default",
                "ea_required_change": "add explicit argmax-compatible probe mode; keep threshold_margin default",
                "mt5_execution_allowed_now": "false",
                "expected_compare_keys": "timestamp;p_short;p_flat;p_long;decision_label;decision_signal;input_hash",
                "source_expected_contract": row["proxy_expected_contract"],
                "watch_policy": row["watch_policy"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_feature_handoff_contract() -> list[dict[str, Any]]:
    features = pd.read_csv(io_path(EH_FEATURE_HANDOFF))
    rows: list[dict[str, Any]] = []
    for row in features.to_dict("records"):
        feature_set = str(row["feature_set_id"])
        included = str(row.get("included_features_json", ""))
        rows.append(
            {
                "feature_set_id": feature_set,
                "feature_count": int(row["feature_count"]),
                "feature_order_hash": row["feature_order_hash"],
                "included_features_sha256": sha256_text(included),
                "source_model_input": row["source_model_input"],
                "common_files_target": f"Project_Obsidian_Prime_v2/stage337/run337EK/features/{feature_set}.csv",
                "strict_header_required": "true",
                "timestamp_policy": "source_model_input_timestamp_utc;exact_match_required",
                "materialization_status": "contract_only_not_written_to_terminal_common_files",
                "effect": "defines terminal handoff without writing runtime files yet(터미널 파일 작성 전 인계 의미를 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_probability_output_audit() -> list[dict[str, Any]]:
    adapter_rows = read_csv(EI_ADAPTER_REVIEW)
    adapter_blocks = sum(1 for row in adapter_rows if as_bool(row.get("blocks_external_mt5")))
    output_order_ok = file_contains(MT5_OUTPUT_CONTRACT, "order = `[p_short, p_flat, p_long]`")
    model_shape_ok = file_contains(MODEL_RUNTIME, "m_probability_shape[1] = 3")
    decision_threshold = file_contains(DECISION_SURFACE, "threshold_or_margin_not_met")
    ea_uses_surface = file_contains(RUNTIME_EA, "g_decision_surface.Evaluate")
    return [
        {
            "audit_id": "mt5_output_order_contract",
            "source_path": rel(MT5_OUTPUT_CONTRACT),
            "observed": "output_order_present" if output_order_ok else "output_order_missing",
            "required_for_argmax_probe": "[p_short,p_flat,p_long]",
            "status": "passed" if output_order_ok else "failed",
            "effect": "output order is already documented(출력 순서는 이미 문서화됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "model_runtime_probability_shape",
            "source_path": rel(MODEL_RUNTIME),
            "observed": "shape_3_supported" if model_shape_ok else "shape_3_missing",
            "required_for_argmax_probe": "three probability values",
            "status": "passed" if model_shape_ok else "failed",
            "effect": "runtime can read 3 probabilities(런타임은 확률 3개를 읽을 수 있음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "current_decision_surface_default",
            "source_path": rel(DECISION_SURFACE),
            "observed": "threshold_margin_default" if decision_threshold else "unknown",
            "required_for_argmax_probe": "keep default; add explicit argmax probe mode",
            "status": "implementation_required" if decision_threshold else "failed",
            "effect": "default surface must not be silently replaced(기본 표면을 몰래 교체하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ea_decision_handoff",
            "source_path": rel(RUNTIME_EA),
            "observed": "uses_decision_surface" if ea_uses_surface else "decision_surface_call_missing",
            "required_for_argmax_probe": "route to argmax mode when configured",
            "status": "implementation_required" if ea_uses_surface else "failed",
            "effect": "EA needs an explicit branch for argmax probe(EA에 argmax 탐침 분기가 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ei_adapter_blocks",
            "source_path": rel(EI_ADAPTER_REVIEW),
            "observed": str(adapter_blocks),
            "required_for_argmax_probe": ">=2 named blocks",
            "status": "passed" if adapter_blocks >= 2 else "failed",
            "effect": "EJ is grounded in the EI blocker(337EJ가 337EI 차단 근거에 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_implementation_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337EK_mqh_argmax_probe_mode",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "add explicit argmax probe mode to decision surface(결정 표면에 명시적 argmax 탐침 모드 추가)",
            "required_inputs": f"{rel(ARGMAX_CONTRACT)};{rel(PROBABILITY_OUTPUT_AUDIT)}",
            "required_outputs": "DecisionSurface.mqh diff;RuntimeProbeEA input routing diff;compile/static review",
            "forbidden_action": "do not change default threshold/margin behavior; no threshold tuning",
            "effect": "repairs parity gap without retuning(재튜닝 없이 동등성 공백 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EK_probe_settings_contract",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize probe settings for argmax mode(argmax 모드 탐침 설정 물질화)",
            "required_inputs": f"{rel(ADAPTER_PROBE_MANIFEST)};{rel(FEATURE_HANDOFF_CONTRACT)}",
            "required_outputs": "set-file or manifest fields naming argmax decision mode",
            "forbidden_action": "no candidate selection; no Forward claim; no live readiness",
            "effect": "makes terminal handoff reviewable(터미널 인계를 검토 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EL_common_files_and_runtime_diff_probe",
            "next_run_id": "run337EL_materialize_common_files_and_run_argmax_parity_probe_without_db_v1",
            "priority": "P1",
            "task": "after EK compile, materialize Common Files and run narrow parity probe(EK 컴파일 후 Common Files와 좁은 동등성 탐침 실행)",
            "required_inputs": f"{rel(FEATURE_HANDOFF_CONTRACT)};{rel(ADAPTER_PROBE_MANIFEST)}",
            "required_outputs": "runtime_probability_tape.csv;runtime_diff_summary.csv",
            "forbidden_action": "no operating promotion; no deployment; no Goal Achieve",
            "effect": "turns static contract into runtime evidence(정적 계약을 런타임 근거로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    ei_final = read_json(EI_FINAL)
    ei_failed_gates = sum(1 for row in read_csv(EI_GATES) if row.get("status") != "passed")
    audit_failed = final["probability_audit_failed_rows"]
    gates = [
        (
            "input_presence",
            final["missing_inputs"] == 0,
            final["missing_inputs"],
            "0",
            "EJ 입력이 모두 있어야 계약을 닫는다.",
        ),
        (
            "parent_ei_gates_passed",
            ei_failed_gates == 0,
            ei_failed_gates,
            "0",
            "부모 EI 게이트가 통과해야 한다.",
        ),
        (
            "parent_next_action_matches",
            ei_final.get("next_action") == RUN_ID,
            ei_final.get("next_action", ""),
            RUN_ID,
            "라우팅이 EJ로 정확히 이어졌는지 확인한다.",
        ),
        (
            "argmax_contract_materialized",
            final["argmax_contract_rows"] >= 8,
            final["argmax_contract_rows"],
            ">=8",
            "argmax 계약 항목이 충분해야 한다.",
        ),
        (
            "adapter_probe_manifest_complete",
            final["adapter_probe_rows"] == 7,
            final["adapter_probe_rows"],
            "7",
            "EH 생존 후보 7개가 모두 이어져야 한다.",
        ),
        (
            "feature_handoff_contract_complete",
            final["feature_handoff_contract_rows"] == 2,
            final["feature_handoff_contract_rows"],
            "2",
            "두 feature set(피처 세트)의 인계 계약이 있어야 한다.",
        ),
        (
            "probability_output_audit_clear_or_implementation_named",
            audit_failed == 0,
            audit_failed,
            "0",
            "출력 감사 실패가 없어야 하며 구현 필요는 이름 붙여야 한다.",
        ),
        (
            "implementation_queue_ready",
            final["implementation_queue_rows"] >= 2,
            final["implementation_queue_rows"],
            ">=2",
            "다음 EK 구현 대기열이 있어야 한다.",
        ),
        (
            "no_forbidden_execution",
            final["mt5_execution"] == "not_run"
            and final["model_training"] == "not_run"
            and final["threshold_tuning"] == "not_run"
            and final["candidate_selection"] == "not_run",
            f"mt5={final['mt5_execution']};training={final['model_training']};threshold={final['threshold_tuning']};selection={final['candidate_selection']}",
            "all_not_run",
            "계약 물질화 단계에서 금지 행동이 없어야 한다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gates
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    payloads = {
        DATA_RECEIPT: {
            "run_id": RUN_ID,
            "status": "passed_contract_inputs_present",
            "source_runtime_manifest_rows": final["adapter_probe_rows"],
            "feature_handoff_contract_rows": final["feature_handoff_contract_rows"],
            "effect": "EJ uses only existing EH/EI artifacts(EJ는 기존 EH/EI 산출물만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        MODEL_RECEIPT: {
            "run_id": RUN_ID,
            "model_training": "not_run",
            "model_selection": "not_run",
            "effect": "no ONNX changed(ONNX 변경 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUNTIME_RECEIPT: {
            "run_id": RUN_ID,
            "runtime_path": [rel(MODEL_RUNTIME), rel(DECISION_SURFACE), rel(RUNTIME_EA)],
            "parity_check": "static_contract_materialized_runtime_not_executed",
            "known_difference": "current EA threshold/margin default still lacks argmax probe mode",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        JUDGMENT_RECEIPT: {
            "result_subject": RUN_ID,
            "evidence_available": [rel(ARGMAX_CONTRACT), rel(ADAPTER_PROBE_MANIFEST), rel(PROBABILITY_OUTPUT_AUDIT)],
            "evidence_missing": "MQL implementation, compile output, runtime probability tape, MT5 tester output",
            "judgment_label": "runtime_probe",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        LINEAGE_RECEIPT: {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in artifact_paths if path_exists(path)],
            "effect": "connects EI blocker to EK implementation queue(EI 차단을 EK 구현 대기열에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }
    return [write_json(path, payload) for path, payload in payloads.items()]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EJ Argmax Adapter Parity Contract(어댑터 동등성 계약)

## Conclusion(결론)

run337EJ(337EJ 실행)는 EI에서 확인한 adapter mismatch(어댑터 불일치)를 좁은 argmax parity contract(argmax 동등성 계약)로 물질화했다. 이 실행은 모델 학습, threshold tuning(임계값 조정), lot optimization(랏 최적화), MT5 execution(MT5 실행)을 하지 않았다.

Action(행동): argmax decision surface contract(argmax 결정 표면 계약), adapter parity probe manifest(어댑터 동등성 탐침 목록), feature Common Files handoff contract(피처 Common Files 인계 계약)을 만들었다.

Effect(효과): 다음 run337EK(337EK 실행)에서 기본 threshold/margin(임계값/마진) 표면을 보존하면서 explicit argmax probe mode(명시적 argmax 탐침 모드)만 추가할 수 있다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- argmax_contract_rows(argmax 계약 행): `{final['argmax_contract_rows']}`
- adapter_probe_rows(어댑터 탐침 행): `{final['adapter_probe_rows']}`
- feature_handoff_contract_rows(피처 인계 계약 행): `{final['feature_handoff_contract_rows']}`
- probability_audit_rows(확률 출력 감사 행): `{final['probability_audit_rows']}`
- implementation_queue_rows(구현 대기열 행): `{final['implementation_queue_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EJ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): argmax parity contract(argmax 동등성 계약)를 만들었지만 EA 구현/컴파일/MT5 실행은 아직 없다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(ARGMAX_CONTRACT)}`, `{rel(ADAPTER_PROBE_MANIFEST)}`, `{rel(PROBABILITY_OUTPUT_AUDIT)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EJ focus complete: argmax adapter parity contract(argmax 어댑터 동등성 계약)를 "
        f"`{final['argmax_contract_rows']}`행으로 물질화했다. Effect(효과): 다음 run337EK에서 기본 threshold/margin(임계값/마진)을 보존한 채 argmax probe mode(argmax 탐침 모드)를 구현한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EJ focus complete")
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
## Stage337 run337EJ(337EJ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): argmax parity contract(argmax 동등성 계약)를 만들었다. 실제 EA 구현/컴파일/MT5/Forward/Goal(실제 EA 구현/컴파일/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EI("
    if "## Stage337 run337EJ(337EJ 실행)" not in current_text:
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
- argmax_contract_rows(argmax 계약 행): `{final["argmax_contract_rows"]}`
- adapter_probe_rows(어댑터 탐침 행): `{final["adapter_probe_rows"]}`
- actual_mt5_execution(실제 MT5 실행): `not_run_ej_contract_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): argmax probe implementation(argmax 탐침 구현)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EJ(337EJ 실행) materialized argmax adapter parity contract(argmax 어댑터 동등성 계약). "
        f"Status(상태) `{STATUS}`. MT5/Forward/Goal(MT5/전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EJ(337EJ 실행) materialized argmax"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EJ materialized argmax adapter parity contract and opened `{NEXT_RUN_ID}` without MT5/Forward claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EJ materialized argmax"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "argmax_adapter_parity_contract_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"argmax_contract_rows={final['argmax_contract_rows']};adapter_probe_rows={final['adapter_probe_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "runtime_parity_artifact_lineage_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_adapter_contract",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "argmax_adapter_contract",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "contract_materialization_no_mt5_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "runtime_parity_contract",
        "scoreboard_lane": "runtime_parity_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"contract_rows={final['argmax_contract_rows']};probe_rows={final['adapter_probe_rows']}",
        "guardrail_kpi": "actual_mt5_not_run;no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "static_contract_only_runtime_not_executed",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_adapter_contract",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_artifact_lineage_result_judgment",
        "evidence_scope": "EI blocker converted into argmax adapter parity contract",
        "kpi_scope": "runtime_parity_contract",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__argmax_adapter_contract",
        "family": "runtime_parity_artifact_lineage_result_judgment",
        "question": "what exact adapter contract is required before external MT5 argmax probe",
        "metric_scope": "argmax_contract_adapter_probe_manifest_feature_handoff_probability_audit",
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
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    argmax_rows = build_argmax_contract()
    probe_rows = build_adapter_probe_manifest()
    feature_rows = build_feature_handoff_contract()
    audit_rows = build_probability_output_audit()
    queue_rows = build_implementation_queue()
    artifacts: list[Path] = [
        write_csv(ARGMAX_CONTRACT, CONTRACT_COLUMNS, argmax_rows),
        write_csv(ADAPTER_PROBE_MANIFEST, PROBE_COLUMNS, probe_rows),
        write_csv(FEATURE_HANDOFF_CONTRACT, FEATURE_COLUMNS, feature_rows),
        write_csv(PROBABILITY_OUTPUT_AUDIT, AUDIT_COLUMNS, audit_rows),
        write_csv(IMPLEMENTATION_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ei_next_action": read_json(EI_FINAL).get("next_action", ""),
        "ei_failed_gate_rows": sum(1 for row in read_csv(EI_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "argmax_contract_rows": len(argmax_rows),
        "adapter_probe_rows": len(probe_rows),
        "feature_handoff_contract_rows": len(feature_rows),
        "probability_audit_rows": len(audit_rows),
        "probability_audit_failed_rows": sum(1 for row in audit_rows if row["status"] == "failed"),
        "probability_audit_implementation_required_rows": sum(1 for row in audit_rows if row["status"] == "implementation_required"),
        "implementation_queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "argmax_contract_rows": final["argmax_contract_rows"],
                "adapter_probe_rows": final["adapter_probe_rows"],
                "implementation_queue_rows": final["implementation_queue_rows"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
