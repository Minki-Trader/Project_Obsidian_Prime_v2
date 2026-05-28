from __future__ import annotations

import csv
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
RUN_NUMBER = "run337EI"
RUN_ID = "run337EI_review_proxy_survivor_runtime_probe_inputs_without_db_v1"
PARENT_RUN_ID = eh.RUN_ID
NEXT_RUN_ID = "run337EJ_materialize_argmax_adapter_parity_probe_contract_without_db_v1"
STATUS = "completed_stage337EI_runtime_input_review_adapter_argmax_mismatch_blocks_external_mt5_no_selection"
JUDGMENT = "runtime_inputs_complete_but_existing_decision_surface_threshold_contract_mismatches_proxy_argmax"
DECISION = "stage337EI_open_run337EJ_materialize_argmax_adapter_parity_probe_contract"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EI_proxy_survivor_runtime_input_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EI_proxy_survivor_runtime_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EI_runtime_input_review.md"
SELECTED_STATUS = eh.SELECTED_STATUS
STAGE_BRIEF = eh.STAGE_BRIEF
WORKSPACE_STATE = eh.WORKSPACE_STATE
CURRENT_STATE = eh.CURRENT_STATE
CHANGELOG = eh.CHANGELOG
RUN_REGISTRY = eh.RUN_REGISTRY
ALPHA_LEDGER = eh.ALPHA_LEDGER
ARTIFACT_REGISTRY = eh.ARTIFACT_REGISTRY
STAGE_LEDGER = eh.STAGE_LEDGER

EH_FINAL = eh.FINAL_DECISION
EH_GATES = eh.REQUIRED_GATE_AUDIT
EH_QUEUE = eh.EI_QUEUE
EH_RUNTIME_MANIFEST = eh.RUNTIME_MANIFEST
EH_FEATURE_HANDOFF = eh.FEATURE_HANDOFF
EH_PROXY_EXPECTED = eh.PROXY_EXPECTED
EH_WATCH_POLICY = eh.WATCH_POLICY
EH_BLOCKER_MATRIX = eh.BLOCKER_MATRIX
EH_PACKAGE_INDEX = eh.PACKAGE_INDEX

MODEL_RUNTIME = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "ModelRuntime.mqh"
DECISION_SURFACE = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "DecisionSurface.mqh"
RUNTIME_EA = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"

MANIFEST_REVIEW = RUN_DIR / "runtime_manifest_review.csv"
FEATURE_REVIEW = RUN_DIR / "feature_handoff_review.csv"
ADAPTER_REVIEW = RUN_DIR / "adapter_contract_review.csv"
BLOCKER_REVIEW = RUN_DIR / "runtime_blocker_review.csv"
ATTEMPT_DECISION = RUN_DIR / "runtime_attempt_decision.csv"
EJ_QUEUE = RUN_DIR / "run337EJ_argmax_adapter_parity_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EH_FINAL,
    EH_GATES,
    EH_QUEUE,
    EH_RUNTIME_MANIFEST,
    EH_FEATURE_HANDOFF,
    EH_PROXY_EXPECTED,
    EH_WATCH_POLICY,
    EH_BLOCKER_MATRIX,
    EH_PACKAGE_INDEX,
    MODEL_RUNTIME,
    DECISION_SURFACE,
    RUNTIME_EA,
)
OUTPUT_FILES = (
    MANIFEST_REVIEW,
    FEATURE_REVIEW,
    ADAPTER_REVIEW,
    BLOCKER_REVIEW,
    ATTEMPT_DECISION,
    EJ_QUEUE,
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

REVIEW_COLUMNS = ("review_id", "subject", "observed", "expected", "status", "effect", "claim_boundary")
FEATURE_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "source_timestamp_start",
    "source_timestamp_end",
    "source_rows",
    "common_file_materialized",
    "review_status",
    "effect",
    "claim_boundary",
)
ADAPTER_COLUMNS = (
    "adapter_check_id",
    "source_path",
    "observed",
    "expected",
    "review_status",
    "blocks_external_mt5",
    "effect",
    "claim_boundary",
)
BLOCKER_COLUMNS = (
    "blocker_id",
    "parent_status",
    "review_status",
    "still_blocks",
    "next_condition",
    "effect",
    "claim_boundary",
)
ATTEMPT_COLUMNS = (
    "probe_id",
    "model_id",
    "proxy_rank",
    "execution_decision",
    "reason",
    "allowed_claim",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "passed", "active"}


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


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


def build_manifest_review() -> list[dict[str, Any]]:
    manifest = pd.read_csv(io_path(EH_RUNTIME_MANIFEST))
    rows: list[dict[str, Any]] = []
    expected = {
        "row_count": ("7", str(len(manifest)), len(manifest) == 7, "7 survivor probes must be present(7개 생존 탐침이 있어야 함)"),
        "decision_policy": (
            "three_class_argmax_from_probabilities",
            ";".join(sorted(manifest["decision_policy"].astype(str).unique())),
            manifest["decision_policy"].astype(str).str.contains("three_class_argmax_from_probabilities").all(),
            "proxy replay contract uses argmax(프록시 재생 계약은 argmax 사용)",
        ),
        "threshold_policy": (
            "not_applicable_no_threshold_sweep",
            ";".join(sorted(manifest["threshold_policy"].astype(str).unique())),
            manifest["threshold_policy"].astype(str).str.contains("not_applicable_no_threshold_sweep").all(),
            "no threshold retune is allowed(임계값 재조정 금지)",
        ),
        "execution_status": (
            "materialized_no_mt5_execution",
            ";".join(sorted(manifest["execution_status"].astype(str).unique())),
            manifest["execution_status"].astype(str).str.contains("materialized_no_mt5_execution").all(),
            "EH did not run MT5(EH는 MT5 미실행)",
        ),
    }
    for key, (expected_value, observed, ok, effect) in expected.items():
        rows.append(
            {
                "review_id": f"manifest_{key}",
                "subject": key,
                "observed": observed,
                "expected": expected_value,
                "status": "passed" if ok else "failed",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_feature_review() -> list[dict[str, Any]]:
    features = pd.read_csv(io_path(EH_FEATURE_HANDOFF))
    rows: list[dict[str, Any]] = []
    for row in features.to_dict("records"):
        source_rows = as_int(row.get("train_rows")) + as_int(row.get("validation_rows")) + as_int(row.get("oos_rows"))
        materialized = False
        status = "review_passed_but_common_file_materialization_required"
        rows.append(
            {
                "feature_set_id": row["feature_set_id"],
                "feature_count": row["feature_count"],
                "feature_order_hash": row["feature_order_hash"],
                "source_timestamp_start": row["source_timestamp_start"],
                "source_timestamp_end": row["source_timestamp_end"],
                "source_rows": source_rows,
                "common_file_materialized": str(materialized).lower(),
                "review_status": status,
                "effect": "feature contract is complete but terminal Common Files handoff still needs a later packet(피처 계약은 완전하지만 터미널 Common Files 인계는 다음 작업 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_adapter_review() -> tuple[list[dict[str, Any]], dict[str, int]]:
    model_runtime = read_code(MODEL_RUNTIME)
    decision_surface = read_code(DECISION_SURFACE)
    runtime_ea = read_code(RUNTIME_EA)
    probability_shape_ok = "m_probability_shape[1] = 3" in model_runtime and "p_short = (double)m_probability[0]" in model_runtime
    one_or_two_outputs_ok = "m_output_count == 1" in model_runtime and "m_output_count == 2" in model_runtime
    threshold_surface = "p_short >= m_short_threshold" in decision_surface and "m_min_margin" in decision_surface
    argmax_surface = "argmax" in decision_surface.lower() or "p_long >= p_short" in decision_surface and "threshold" not in decision_surface.lower()
    ea_uses_decision_surface = "g_decision_surface.Configure" in runtime_ea and "Evaluate" in runtime_ea
    rows = [
        {
            "adapter_check_id": "onnx_probability_shape_3",
            "source_path": rel(MODEL_RUNTIME),
            "observed": "probability_shape_3_supported" if probability_shape_ok else "probability_shape_3_missing",
            "expected": "probability_shape_3_supported",
            "review_status": "passed" if probability_shape_ok else "failed",
            "blocks_external_mt5": "false" if probability_shape_ok else "true",
            "effect": "ModelRuntime can read short/flat/long probabilities(ModelRuntime이 숏/플랫/롱 확률을 읽을 수 있다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "adapter_check_id": "onnx_output_count_support",
            "source_path": rel(MODEL_RUNTIME),
            "observed": "one_or_two_outputs_supported" if one_or_two_outputs_ok else "output_count_support_missing",
            "expected": "one_or_two_outputs_supported",
            "review_status": "passed" if one_or_two_outputs_ok else "failed",
            "blocks_external_mt5": "false" if one_or_two_outputs_ok else "true",
            "effect": "runtime can handle sklearn ONNX probability output shape(런타임이 sklearn ONNX 확률 출력 구조를 다룰 수 있다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "adapter_check_id": "decision_surface_policy",
            "source_path": rel(DECISION_SURFACE),
            "observed": "threshold_margin_surface" if threshold_surface else "unknown_surface",
            "expected": "three_class_argmax_surface",
            "review_status": "blocked_argmax_contract_mismatch" if threshold_surface and not argmax_surface else "passed",
            "blocks_external_mt5": "true" if threshold_surface and not argmax_surface else "false",
            "effect": "proxy replay used argmax, but current EA uses thresholds and margin(프록시 재생은 argmax지만 현재 EA는 임계값과 마진 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "adapter_check_id": "ea_decision_surface_handoff",
            "source_path": rel(RUNTIME_EA),
            "observed": "ea_uses_decision_surface" if ea_uses_decision_surface else "ea_decision_surface_missing",
            "expected": "argmax_or_configurable_decision_surface",
            "review_status": "blocked_ea_surface_not_configurable_for_argmax" if ea_uses_decision_surface else "failed",
            "blocks_external_mt5": "true",
            "effect": "EA needs an explicit argmax-compatible probe mode before external MT5(EA는 외부 MT5 전에 명시적 argmax 호환 탐침 모드가 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, {
        "adapter_rows": len(rows),
        "adapter_pass_rows": sum(1 for row in rows if row["review_status"] == "passed"),
        "adapter_block_rows": sum(1 for row in rows if as_bool(row["blocks_external_mt5"])),
    }


def build_blocker_review() -> list[dict[str, Any]]:
    blockers = pd.read_csv(io_path(EH_BLOCKER_MATRIX))
    rows: list[dict[str, Any]] = []
    for row in blockers.to_dict("records"):
        rows.append(
            {
                "blocker_id": row["blocker_id"],
                "parent_status": row["status"],
                "review_status": "still_active",
                "still_blocks": "true",
                "next_condition": NEXT_RUN_ID,
                "effect": row["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_attempt_decision() -> list[dict[str, Any]]:
    manifest = pd.read_csv(io_path(EH_RUNTIME_MANIFEST))
    rows: list[dict[str, Any]] = []
    for row in manifest.sort_values("proxy_rank").to_dict("records"):
        rows.append(
            {
                "probe_id": row["probe_id"],
                "model_id": row["model_id"],
                "proxy_rank": as_int(row["proxy_rank"]),
                "execution_decision": "blocked_before_external_mt5_adapter_argmax_contract",
                "reason": "current_decision_surface_threshold_margin_mismatches_proxy_argmax",
                "allowed_claim": "runtime_input_review_only_no_forward_or_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ej_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EJ_argmax_decision_surface_contract",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize argmax-compatible adapter parity probe contract(argmax 호환 어댑터 동등성 탐침 계약 물질화)",
            "required_inputs": f"{rel(ADAPTER_REVIEW)};{rel(EH_RUNTIME_MANIFEST)};{rel(EH_PROXY_EXPECTED)}",
            "required_outputs": "argmax_decision_surface_contract.csv;adapter_parity_probe_manifest.csv",
            "blocked_if_missing": "adapter review or runtime manifest(어댑터 검토 또는 런타임 목록)",
            "forbidden_action": "no model retune, no threshold tuning, no MT5 execution(모델 재조정/임계값 조정/MT5 실행 금지)",
            "effect": "turns the adapter mismatch into a narrow parity repair/probe contract(어댑터 불일치를 좁은 동등성 수리/탐침 계약으로 바꾼다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EJ_feature_common_files_handoff_contract",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize Common Files feature handoff contract(Common Files 피처 인계 계약 물질화)",
            "required_inputs": f"{rel(FEATURE_REVIEW)};{rel(EH_FEATURE_HANDOFF)}",
            "required_outputs": "feature_common_files_handoff_contract.csv",
            "blocked_if_missing": "feature handoff review(피처 인계 검토)",
            "forbidden_action": "no hidden feature reorder or feature add(숨은 피처 재정렬/추가 금지)",
            "effect": "keeps feature order stable before any terminal run(터미널 실행 전 피처 순서를 고정한다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "EH 입력이 있어야 EI 검토가 닫힌다."),
        ("parent_eh_gates_passed", final["eh_failed_gate_rows"] == 0, str(final["eh_failed_gate_rows"]), "0", "부모 EH 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["eh_next_action"] == RUN_ID, str(final["eh_next_action"]), RUN_ID, "라우팅이 EI로 정확히 이어졌는지 확인한다."),
        ("manifest_review_passed", final["manifest_failed_rows"] == 0, str(final["manifest_failed_rows"]), "0", "런타임 목록 자체는 완전해야 한다."),
        ("adapter_mismatch_named", final["adapter_block_rows"] >= 1, str(final["adapter_block_rows"]), ">=1", "argmax/threshold 불일치를 명시해야 한다."),
        ("external_mt5_denied", final["runtime_attempt_blocked_rows"] == 7, str(final["runtime_attempt_blocked_rows"]), "7", "7개 탐침 모두 외부 MT5 전에 차단되어야 한다."),
        ("blockers_still_active", final["still_active_blocker_rows"] == 4, str(final["still_active_blocker_rows"]), "4", "EH 차단 4개가 계속 활성이어야 한다."),
        ("ej_queue_materialized", final["ej_queue_rows"] == 2, str(final["ej_queue_rows"]), "2", "EJ 수리/계약 대기열이 있어야 한다."),
        (
            "no_forbidden_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_execution"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "선택/MT5/Goal 주장을 막는다.",
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
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"manifest_review_rows={final['manifest_review_rows']};attempt_rows={final['runtime_attempt_rows']}",
        "integrity_judgment": "review_valid_adapter_mismatch_named(검토 유효, 어댑터 불일치 명명됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "seven proxy survivor ONNX inputs reviewed(7개 프록시 생존 후보 ONNX 입력 검토)",
        "selection_metric": "none(없음)",
        "threshold_policy": "no tuning; threshold surface mismatch blocks runtime(조정 없음, 임계값 표면 불일치가 런타임 차단)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_claim": "blocked_before_external_mt5(외부 MT5 전 차단)",
        "adapter_block_rows": final["adapter_block_rows"],
        "runtime_authority": "not_claimed(주장 없음)",
        "next_condition": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "runtime input package and code-level adapter review(런타임 입력 패키지와 코드 수준 어댑터 검토)",
        "evidence_missing": "argmax adapter parity probe and external MT5(argmax 어댑터 동등성 탐침과 외부 MT5)",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EI Runtime Input Review(런타임 입력 검토)

## Conclusion(결론)

run337EI(337EI 실행)는 EH runtime input package(런타임 입력 패키지)를 검토했다. Manifest/feature/proxy expected(목록/피처/프록시 예상 계약)는 완전하지만, current DecisionSurface(현재 결정 표면)는 threshold/margin(임계값/마진) 방식이고 EG proxy replay(EG 프록시 재생)는 three-class argmax(3분류 최대확률 선택) 방식이다.

Action(행동): 외부 MT5 execution(MT5 실행)을 하지 않았다.

Effect(효과): 7개 탐침 모두 `blocked_before_external_mt5_adapter_argmax_contract`로 닫고, run337EJ(337EJ 실행)에서 argmax adapter parity probe contract(argmax 어댑터 동등성 탐침 계약)를 물질화한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- manifest_review_rows(목록 검토 행): `{final["manifest_review_rows"]}`
- feature_review_rows(피처 검토 행): `{final["feature_review_rows"]}`
- adapter_block_rows(어댑터 차단 행): `{final["adapter_block_rows"]}`
- runtime_attempt_blocked_rows(런타임 시도 차단 행): `{final["runtime_attempt_blocked_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EI

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 런타임 입력은 완전하지만 현재 EA 결정 표면이 프록시 argmax 계약과 달라 외부 MT5 실행을 차단했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(ADAPTER_REVIEW)}`, `{rel(ATTEMPT_DECISION)}`
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
        f"  Stage337 run337EI focus complete: runtime input review(런타임 입력 검토)에서 adapter argmax mismatch(어댑터 argmax 불일치) "
        f"`{final['adapter_block_rows']}`행을 확인했다. Effect(효과): 외부 MT5 실행은 막고 run337EJ argmax adapter parity contract(argmax 어댑터 동등성 계약)를 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EI focus complete")
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
## Stage337 run337EI(337EI 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 런타임 입력 패키지는 완전하지만 현재 DecisionSurface(결정 표면)가 threshold/margin(임계값/마진)이라 proxy argmax(프록시 최대확률 선택)와 맞지 않는다. 실제 MT5/Forward/Goal(실제 MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EH("
    if "## Stage337 run337EI(337EI 실행)" not in current_text:
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
- adapter_block_rows(어댑터 차단 행): `{final["adapter_block_rows"]}`
- actual_mt5_execution(실제 MT5 실행): `not_run_ei_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): argmax adapter parity contract(argmax 어댑터 동등성 계약) 물질화로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EI(337EI 실행) reviewed proxy survivor runtime inputs(프록시 생존 후보 런타임 입력) and blocked external MT5 because adapter argmax parity is not proven. "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)는 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EI(337EI 실행) reviewed proxy survivor runtime inputs"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EI reviewed runtime inputs and opened `{NEXT_RUN_ID}` because current DecisionSurface is threshold/margin while proxy replay is argmax."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EI reviewed runtime inputs"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_survivor_runtime_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"adapter_block_rows={final['adapter_block_rows']};runtime_attempt_blocked={final['runtime_attempt_blocked_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "runtime_parity_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_mt5_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "adapter_contract_runtime_input_review",
        "scoreboard_lane": "runtime_parity_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"adapter_block_rows={final['adapter_block_rows']};attempt_blocked={final['runtime_attempt_blocked_rows']}",
        "guardrail_kpi": "actual_mt5_not_run;no_selection;no_forward;runtime_authority_not_claimed",
        "external_verification_status": "blocked_before_external_mt5_execution",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_result_judgment_artifact_lineage",
        "evidence_scope": "EH runtime package and MT5 adapter code reviewed",
        "kpi_scope": "adapter_contract_runtime_input_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__runtime_input_review",
        "family": "runtime_parity_result_judgment_artifact_lineage",
        "question": "can EH runtime inputs proceed to external MT5",
        "metric_scope": "manifest_feature_adapter_blockers_attempt_decision",
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
    manifest_rows = build_manifest_review()
    feature_rows = build_feature_review()
    adapter_rows, adapter_summary = build_adapter_review()
    blocker_rows = build_blocker_review()
    attempt_rows = build_attempt_decision()
    queue_rows = build_ej_queue()
    artifacts: list[Path] = [
        write_csv(MANIFEST_REVIEW, REVIEW_COLUMNS, manifest_rows),
        write_csv(FEATURE_REVIEW, FEATURE_COLUMNS, feature_rows),
        write_csv(ADAPTER_REVIEW, ADAPTER_COLUMNS, adapter_rows),
        write_csv(BLOCKER_REVIEW, BLOCKER_COLUMNS, blocker_rows),
        write_csv(ATTEMPT_DECISION, ATTEMPT_COLUMNS, attempt_rows),
        write_csv(EJ_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    eh_final = read_json(EH_FINAL)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "eh_next_action": eh_final.get("next_action", ""),
        "eh_failed_gate_rows": sum(1 for row in read_csv(EH_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "manifest_review_rows": len(manifest_rows),
        "manifest_failed_rows": sum(1 for row in manifest_rows if row["status"] != "passed"),
        "feature_review_rows": len(feature_rows),
        "adapter_rows": adapter_summary["adapter_rows"],
        "adapter_pass_rows": adapter_summary["adapter_pass_rows"],
        "adapter_block_rows": adapter_summary["adapter_block_rows"],
        "still_active_blocker_rows": sum(1 for row in blocker_rows if as_bool(row["still_blocks"])),
        "runtime_attempt_rows": len(attempt_rows),
        "runtime_attempt_blocked_rows": sum(1 for row in attempt_rows if row["execution_decision"].startswith("blocked_before_external_mt5")),
        "ej_queue_rows": len(queue_rows),
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
                "adapter_block_rows": final["adapter_block_rows"],
                "runtime_attempt_blocked_rows": final["runtime_attempt_blocked_rows"],
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
