from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_argmax_adapter_parity_probe_contract as ej  # noqa: E402
from stage_pipelines.stage337 import materialize_proxy_survivor_row_level_runtime_probe_inputs as eh  # noqa: E402
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
RUN_NUMBER = "run337EK"
RUN_ID = "run337EK_implement_argmax_probe_decision_surface_without_db_v1"
PARENT_RUN_ID = ej.RUN_ID
NEXT_RUN_ID = "run337EL_materialize_common_files_and_run_argmax_parity_probe_without_db_v1"
STATUS = "completed_stage337EK_argmax_probe_decision_surface_implemented_compiled_no_mt5_probe_no_selection"
JUDGMENT = "argmax_probe_mode_implemented_and_metaeditor_compiled_but_runtime_parity_not_executed"
DECISION = "stage337EK_open_run337EL_materialize_common_files_and_run_argmax_parity_probe"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EK_argmax_probe_decision_surface_implementation_without_db_"
    "metaeditor_compile_only_no_strategy_tester_no_runtime_probe_execution_no_new_training_"
    "no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EK_argmax_probe_decision_surface_implementation.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EK_argmax_probe_decision_surface.md"
SELECTED_STATUS = eh.SELECTED_STATUS
STAGE_BRIEF = eh.STAGE_BRIEF
WORKSPACE_STATE = eh.WORKSPACE_STATE
CURRENT_STATE = eh.CURRENT_STATE
CHANGELOG = eh.CHANGELOG
RUN_REGISTRY = eh.RUN_REGISTRY
ALPHA_LEDGER = eh.ALPHA_LEDGER
ARTIFACT_REGISTRY = eh.ARTIFACT_REGISTRY
STAGE_LEDGER = eh.STAGE_LEDGER

EJ_FINAL = ej.FINAL_DECISION
EJ_GATES = ej.REQUIRED_GATE_AUDIT
EJ_ARGMAX_CONTRACT = ej.ARGMAX_CONTRACT
EJ_ADAPTER_PROBE_MANIFEST = ej.ADAPTER_PROBE_MANIFEST
EJ_FEATURE_HANDOFF_CONTRACT = ej.FEATURE_HANDOFF_CONTRACT
EJ_PROBABILITY_OUTPUT_AUDIT = ej.PROBABILITY_OUTPUT_AUDIT
EJ_IMPLEMENTATION_QUEUE = ej.IMPLEMENTATION_QUEUE

MODEL_RUNTIME = ej.MODEL_RUNTIME
DECISION_SURFACE = ej.DECISION_SURFACE
RUNTIME_EA = ej.RUNTIME_EA
COMPILE_LOG = RUN_DIR / "metaeditor_compile_runtimeprobeea.log"

STATIC_REVIEW = RUN_DIR / "mql_static_argmax_probe_review.csv"
SETTINGS_CONTRACT = RUN_DIR / "argmax_probe_settings_contract.csv"
COMPILE_REVIEW = RUN_DIR / "metaeditor_compile_review.csv"
EL_QUEUE = RUN_DIR / "run337EL_runtime_parity_probe_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EJ_FINAL,
    EJ_GATES,
    EJ_ARGMAX_CONTRACT,
    EJ_ADAPTER_PROBE_MANIFEST,
    EJ_FEATURE_HANDOFF_CONTRACT,
    EJ_PROBABILITY_OUTPUT_AUDIT,
    EJ_IMPLEMENTATION_QUEUE,
    DECISION_SURFACE,
    RUNTIME_EA,
    MODEL_RUNTIME,
    COMPILE_LOG,
)
OUTPUT_FILES = (
    STATIC_REVIEW,
    SETTINGS_CONTRACT,
    COMPILE_REVIEW,
    EL_QUEUE,
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
    DECISION_SURFACE,
    RUNTIME_EA,
    Path(__file__),
)

STATIC_COLUMNS = (
    "review_id",
    "source_path",
    "observed",
    "expected",
    "status",
    "effect",
    "claim_boundary",
)
SETTINGS_COLUMNS = (
    "setting_name",
    "required_for_argmax_probe",
    "default_value",
    "scope",
    "status",
    "effect",
    "claim_boundary",
)
COMPILE_COLUMNS = (
    "compile_id",
    "ea_path",
    "compile_log_path",
    "errors",
    "warnings",
    "result_status",
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


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def read_code(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_compile_log() -> str:
    raw = io_path(COMPILE_LOG).read_bytes()
    for encoding in ("utf-16", "utf-8-sig", "cp949", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def compile_result() -> dict[str, Any]:
    text = read_compile_log()
    match = re.search(r"Result:\s*(\d+)\s+errors,\s*(\d+)\s+warnings", text)
    errors = int(match.group(1)) if match else -1
    warnings = int(match.group(2)) if match else -1
    return {
        "errors": errors,
        "warnings": warnings,
        "passed": errors == 0 and warnings == 0,
        "tail": "\n".join(text.splitlines()[-12:]),
    }


def static_review_rows() -> list[dict[str, Any]]:
    surface = read_code(DECISION_SURFACE)
    ea = read_code(RUNTIME_EA)
    evaluate_pos = surface.find("void Evaluate(")
    invalid_guard_pos = surface.find('result.reason = "probability_invalid"', evaluate_pos)
    argmax_branch_pos = surface.find("if(IsArgmaxProbeMode())", evaluate_pos)
    checks = [
        (
            "decision_mode_field",
            DECISION_SURFACE,
            "m_decision_mode" in surface and "threshold_margin" in surface,
            "m_decision_mode with threshold_margin default",
            "keeps default mode explicit(기본 모드를 명시)",
        ),
        (
            "argmax_probe_evaluator",
            DECISION_SURFACE,
            "EvaluateArgmax" in surface and "argmax_probe_long" in surface and "argmax_probe_short" in surface,
            "EvaluateArgmax with long/short/flat labels",
            "adds explicit argmax path(명시적 argmax 경로 추가)",
        ),
        (
            "tie_rule_first_max",
            DECISION_SURFACE,
            "p_flat > confidence" in surface and "p_long > confidence" in surface,
            "strict greater comparisons preserve first max",
            "matches contract tie rule(계약의 동률 규칙과 맞춤)",
        ),
        (
            "invalid_guard_before_argmax",
            DECISION_SURFACE,
            evaluate_pos >= 0 and invalid_guard_pos >= 0 and argmax_branch_pos >= 0 and invalid_guard_pos < argmax_branch_pos,
            "invalid probability guard before argmax mode",
            "keeps fail-safe before decision(결정 전 안전장치 유지)",
        ),
        (
            "threshold_default_preserved",
            DECISION_SURFACE,
            "threshold_or_margin_not_met" in surface and "p_short >= m_short_threshold" in surface,
            "threshold/margin path remains present",
            "prevents default behavior replacement(기본 동작 교체 방지)",
        ),
        (
            "ea_primary_input_default",
            RUNTIME_EA,
            'InpDecisionMode = "threshold_margin"' in ea,
            "InpDecisionMode default threshold_margin",
            "keeps new mode opt-in(새 모드는 선택식)",
        ),
        (
            "ea_fallback_input_default",
            RUNTIME_EA,
            'InpFallbackDecisionMode = "threshold_margin"' in ea,
            "InpFallbackDecisionMode default threshold_margin",
            "keeps fallback default stable(대체 경로 기본값 유지)",
        ),
        (
            "ea_primary_configures_mode",
            RUNTIME_EA,
            "g_decision_surface.ConfigureDecisionMode(InpDecisionMode)" in ea,
            "primary surface receives decision mode",
            "connects input to runtime branch(입력을 런타임 분기에 연결)",
        ),
        (
            "ea_fallback_configures_mode",
            RUNTIME_EA,
            "g_fallback_decision_surface.ConfigureDecisionMode(InpFallbackDecisionMode)" in ea,
            "fallback surface receives decision mode",
            "connects fallback input to runtime branch(대체 입력을 런타임 분기에 연결)",
        ),
    ]
    return [
        {
            "review_id": review_id,
            "source_path": rel(path),
            "observed": "present" if passed else "missing_or_order_failed",
            "expected": expected,
            "status": "passed" if passed else "failed",
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for review_id, path, passed, expected, effect in checks
    ]


def settings_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("InpDecisionMode", "argmax_probe", "threshold_margin", "primary", "argmax path must be explicitly enabled(명시적으로 argmax 경로를 켜야 함)"),
        ("InpFallbackDecisionMode", "argmax_probe if fallback enabled", "threshold_margin", "fallback", "fallback must use same interpretation when active(활성 대체 경로도 같은 해석 필요)"),
        ("InpInvertSignal", "false", "false", "primary", "class order must stay short/flat/long(클래스 순서 유지)"),
        ("InpFallbackInvertSignal", "false", "false", "fallback", "fallback class order must stay stable(대체 클래스 순서 유지)"),
        ("InpSideFilterEnabled", "false for first parity probe", "false", "shared", "side filters would change proxy decisions(사이드 필터는 프록시 결정을 바꿈)"),
        ("InpAllowTrading", "false for probability parity first", "true", "probe", "probability/decision tape precedes trading claims(확률/결정 테이프가 거래 주장보다 먼저)"),
        ("InpTelemetryEnabled", "true", "true", "probe", "runtime diff needs telemetry(런타임 차이 검토에 텔레메트리 필요)"),
        ("InpFeatureStrictHeader", "true", "true", "feature handoff", "blocks hidden feature reorder(숨은 피처 재정렬 차단)"),
    ]
    return [
        {
            "setting_name": name,
            "required_for_argmax_probe": required,
            "default_value": default,
            "scope": scope,
            "status": "materialized_contract",
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, required, default, scope, effect in rows
    ]


def compile_review_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "compile_id": "metaeditor_runtimeprobeea_compile",
            "ea_path": rel(RUNTIME_EA),
            "compile_log_path": rel(COMPILE_LOG),
            "errors": result["errors"],
            "warnings": result["warnings"],
            "result_status": "passed" if result["passed"] else "failed",
            "effect": "MetaEditor compile validates MQL syntax only(MetaEditor 컴파일은 MQL 문법만 검증)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def el_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337EL_common_files_feature_handoff",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize feature CSVs into terminal Common Files(피처 CSV를 터미널 Common Files로 물질화)",
            "required_inputs": f"{rel(EJ_FEATURE_HANDOFF_CONTRACT)};{rel(EJ_ADAPTER_PROBE_MANIFEST)}",
            "required_outputs": "feature CSVs with strict header;feature handoff receipt",
            "forbidden_action": "no feature reorder; no feature add; no model retrain",
            "effect": "makes EA input reproducible(EA 입력을 재현 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EL_argmax_probability_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "run narrow argmax runtime parity probe(좁은 argmax 런타임 동등성 탐침 실행)",
            "required_inputs": f"{rel(SETTINGS_CONTRACT)};{rel(COMPILE_REVIEW)}",
            "required_outputs": "runtime_probability_tape.csv;runtime_diff_summary.csv;tester or terminal output",
            "forbidden_action": "no Forward Passed/Failed; no operating promotion; no deployment",
            "effect": "tests Python-to-EA meaning before trading claims(Python-EA 의미를 거래 주장 전 검증)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EL_proxy_expected_comparison",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "compare runtime probability/decision tape against proxy contract(런타임 확률/결정 테이프를 프록시 계약과 비교)",
            "required_inputs": f"{rel(EJ_ARGMAX_CONTRACT)};{rel(EJ_ADAPTER_PROBE_MANIFEST)}",
            "required_outputs": "runtime_diff_summary.csv with mismatches/tie_count/nonfinite_count",
            "forbidden_action": "no KPI promotion from parity-only run",
            "effect": "separates parity evidence from profitability evidence(동등성 근거와 수익성 근거 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    ej_final = read_json(EJ_FINAL)
    ej_failed_gates = sum(1 for row in read_csv(EJ_GATES) if row.get("status") != "passed")
    gates = [
        (
            "input_presence",
            final["missing_inputs"] == 0,
            final["missing_inputs"],
            "0",
            "EK 입력과 컴파일 로그가 있어야 한다.",
        ),
        (
            "parent_ej_gates_passed",
            ej_failed_gates == 0,
            ej_failed_gates,
            "0",
            "부모 EJ 게이트가 통과해야 한다.",
        ),
        (
            "parent_next_action_matches",
            ej_final.get("next_action") == RUN_ID,
            ej_final.get("next_action", ""),
            RUN_ID,
            "라우팅이 EK로 정확히 이어졌는지 확인한다.",
        ),
        (
            "static_review_passed",
            final["static_failed_rows"] == 0,
            final["static_failed_rows"],
            "0",
            "MQL 정적 검토가 통과해야 한다.",
        ),
        (
            "metaeditor_compile_passed",
            final["compile_errors"] == 0 and final["compile_warnings"] == 0,
            f"errors={final['compile_errors']};warnings={final['compile_warnings']}",
            "errors=0;warnings=0",
            "MetaEditor 컴파일이 오류/경고 없이 통과해야 한다.",
        ),
        (
            "default_surface_preserved",
            final["default_surface_preserved"] == "true",
            final["default_surface_preserved"],
            "true",
            "기본 threshold/margin 동작이 남아 있어야 한다.",
        ),
        (
            "settings_contract_ready",
            final["settings_contract_rows"] >= 8,
            final["settings_contract_rows"],
            ">=8",
            "EL 실행 설정 계약이 있어야 한다.",
        ),
        (
            "el_queue_ready",
            final["el_queue_rows"] >= 3,
            final["el_queue_rows"],
            ">=3",
            "다음 런타임 동등성 탐침 대기열이 있어야 한다.",
        ),
        (
            "no_forbidden_runtime_claim",
            final["strategy_tester_execution"] == "not_run" and final["runtime_authority"] == "not_claimed",
            f"strategy_tester={final['strategy_tester_execution']};authority={final['runtime_authority']}",
            "not_run;not_claimed",
            "컴파일을 런타임 권위로 과장하지 않는다.",
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
            "status": "passed_static_inputs_present",
            "effect": "EK reads EJ contracts and local compile log(EK는 EJ 계약과 로컬 컴파일 로그를 읽음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        MODEL_RECEIPT: {
            "run_id": RUN_ID,
            "model_training": "not_run",
            "onnx_changed": "false",
            "effect": "implementation touched adapter only(어댑터만 변경)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUNTIME_RECEIPT: {
            "run_id": RUN_ID,
            "runtime_path": [rel(DECISION_SURFACE), rel(RUNTIME_EA)],
            "parity_check": "metaeditor_compile_and_static_review_only",
            "compile_log": rel(COMPILE_LOG),
            "runtime_claim_boundary": "runtime_probe_not_executed_no_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        JUDGMENT_RECEIPT: {
            "result_subject": RUN_ID,
            "evidence_available": [rel(STATIC_REVIEW), rel(COMPILE_REVIEW), rel(REPORT_PATH)],
            "evidence_missing": "Common Files handoff, runtime probability tape, Strategy Tester output, runtime diff summary",
            "judgment_label": "runtime_probe",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        LINEAGE_RECEIPT: {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in artifact_paths if path_exists(path)],
            "effect": "connects EJ contract to MQL implementation and EL runtime probe queue(EJ 계약을 MQL 구현과 EL 탐침 대기열에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }
    return [write_json(path, payload) for path, payload in payloads.items()]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EK Argmax Probe Decision Surface(결정 표면 구현)

## Conclusion(결론)

run337EK(337EK 실행)는 EJ contract(EJ 계약)에 맞춰 RuntimeProbeEA(런타임 탐침 EA)에 explicit argmax probe mode(명시적 argmax 탐침 모드)를 추가했다. 기본 DecisionSurface(결정 표면)는 `threshold_margin(임계값/마진)`으로 유지된다.

Action(행동): MQL adapter(MQL 어댑터)를 수정하고 MetaEditor compile(MetaEditor 컴파일)을 실행했다.

Effect(효과): 컴파일 기준으로 구현은 통과했지만, runtime parity(런타임 동등성)는 아직 실행하지 않았다. 다음 run337EL(337EL 실행)에서 Common Files(공통 파일) 인계와 runtime probability tape(런타임 확률 테이프)를 만든다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- static_review_rows(정적 검토 행): `{final['static_review_rows']}`
- static_failed_rows(정적 실패 행): `{final['static_failed_rows']}`
- compile_errors(컴파일 오류): `{final['compile_errors']}`
- compile_warnings(컴파일 경고): `{final['compile_warnings']}`
- settings_contract_rows(설정 계약 행): `{final['settings_contract_rows']}`
- el_queue_rows(EL 대기열 행): `{final['el_queue_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EK

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): argmax probe mode(argmax 탐침 모드)는 구현/컴파일됐지만 runtime parity(런타임 동등성)는 다음 실행으로 남는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(STATIC_REVIEW)}`, `{rel(COMPILE_REVIEW)}`, `{rel(COMPILE_LOG)}`
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
        f"  Stage337 run337EK focus complete: argmax probe mode(argmax 탐침 모드)를 MQL에 구현했고 MetaEditor compile(MetaEditor 컴파일) "
        f"`{final['compile_errors']}` errors / `{final['compile_warnings']}` warnings(오류/경고)로 통과했다. Effect(효과): 다음 run337EL에서 Common Files 인계와 런타임 확률 테이프를 검증한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EK focus complete")
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
## Stage337 run337EK(337EK 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): argmax probe mode(argmax 탐침 모드)를 구현하고 MetaEditor compile(MetaEditor 컴파일)을 통과했다. Strategy Tester/Forward/Goal(전략 테스터/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EJ("
    if "## Stage337 run337EK(337EK 실행)" not in current_text:
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
- argmax_probe_mode(argmax 탐침 모드): `implemented_compile_passed`
- compile_errors(컴파일 오류): `{final["compile_errors"]}`
- compile_warnings(컴파일 경고): `{final["compile_warnings"]}`
- actual_mt5_execution(실제 MT5 실행): `metaeditor_compile_only_no_strategy_tester`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): runtime parity probe(런타임 동등성 탐침)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EK(337EK 실행) implemented argmax probe mode(argmax 탐침 모드) and MetaEditor compile(MetaEditor 컴파일) passed "
        f"`{final['compile_errors']}` errors / `{final['compile_warnings']}` warnings. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EK(337EK 실행) implemented argmax"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EK implemented argmax probe mode in the runtime EA and passed MetaEditor compile; opened `{NEXT_RUN_ID}` without runtime authority."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EK implemented argmax"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "argmax_probe_decision_surface_implementation_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"compile_errors={final['compile_errors']};compile_warnings={final['compile_warnings']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "runtime_parity_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_probe_implementation",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "argmax_probe_implementation",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mql_implementation_compile_no_mt5_probe",
        "tier_scope": "out_of_scope_by_claim_no_runtime_probe",
        "kpi_scope": "mql_static_compile",
        "scoreboard_lane": "runtime_parity_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"compile_errors={final['compile_errors']};compile_warnings={final['compile_warnings']}",
        "guardrail_kpi": "strategy_tester_not_run;no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "metaeditor_compile_only",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__argmax_probe_implementation",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_result_judgment_artifact_lineage",
        "evidence_scope": "MQL implementation, static review, MetaEditor compile log",
        "kpi_scope": "mql_static_compile",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__argmax_probe_implementation",
        "family": "runtime_parity_result_judgment_artifact_lineage",
        "question": "does the runtime EA now support explicit argmax probe mode",
        "metric_scope": "mql_static_review_metaeditor_compile_settings_contract",
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
    static_rows = static_review_rows()
    settings_rows = settings_contract_rows()
    compile_info = compile_result()
    compile_rows = compile_review_rows(compile_info)
    queue_rows = el_queue_rows()
    artifacts: list[Path] = [
        write_csv(STATIC_REVIEW, STATIC_COLUMNS, static_rows),
        write_csv(SETTINGS_CONTRACT, SETTINGS_COLUMNS, settings_rows),
        write_csv(COMPILE_REVIEW, COMPILE_COLUMNS, compile_rows),
        write_csv(EL_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ej_next_action": read_json(EJ_FINAL).get("next_action", ""),
        "ej_failed_gate_rows": sum(1 for row in read_csv(EJ_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "static_review_rows": len(static_rows),
        "static_failed_rows": sum(1 for row in static_rows if row["status"] != "passed"),
        "settings_contract_rows": len(settings_rows),
        "compile_errors": compile_info["errors"],
        "compile_warnings": compile_info["warnings"],
        "compile_log_path": rel(COMPILE_LOG),
        "el_queue_rows": len(queue_rows),
        "default_surface_preserved": "true" if any(row["review_id"] == "threshold_default_preserved" and row["status"] == "passed" for row in static_rows) else "false",
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "metaeditor_compile": "run",
        "strategy_tester_execution": "not_run",
        "runtime_probe_execution": "not_run",
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
    artifacts.extend(build_receipts(final, artifacts + [COMPILE_LOG, DECISION_SURFACE, RUNTIME_EA]))
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts + [COMPILE_LOG, DECISION_SURFACE, RUNTIME_EA], final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "compile_errors": final["compile_errors"],
                "compile_warnings": final["compile_warnings"],
                "static_failed_rows": final["static_failed_rows"],
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
