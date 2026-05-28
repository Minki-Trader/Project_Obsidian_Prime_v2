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
from stage_pipelines.stage337 import review_proxy_survivor_attribution_package_precheck as eg  # noqa: E402
from stage_pipelines.stage337 import train_validation_density_trade_count_repair_candidates as ee  # noqa: E402
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
STAGE_ID = eg.STAGE_ID
RUN_NUMBER = "run337EH"
RUN_ID = "run337EH_materialize_proxy_survivor_row_level_runtime_probe_inputs_without_db_v1"
PARENT_RUN_ID = eg.RUN_ID
NEXT_RUN_ID = "run337EI_review_proxy_survivor_runtime_probe_inputs_without_db_v1"
STATUS = "completed_stage337EH_proxy_survivor_runtime_probe_inputs_materialized_no_mt5_no_selection"
JUDGMENT = "runtime_probe_inputs_materialized_but_adapter_and_external_mt5_review_required_no_authority"
DECISION = "stage337EH_open_run337EI_review_proxy_survivor_runtime_probe_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EH_proxy_survivor_runtime_probe_input_materialization_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eg.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EH_proxy_survivor_runtime_probe_input_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EH_runtime_probe_input_materialization.md"
SELECTED_STATUS = eg.SELECTED_STATUS
STAGE_BRIEF = eg.STAGE_BRIEF
WORKSPACE_STATE = eg.WORKSPACE_STATE
CURRENT_STATE = eg.CURRENT_STATE
CHANGELOG = eg.CHANGELOG
RUN_REGISTRY = eg.RUN_REGISTRY
ALPHA_LEDGER = eg.ALPHA_LEDGER
ARTIFACT_REGISTRY = eg.ARTIFACT_REGISTRY
STAGE_LEDGER = eg.STAGE_LEDGER

EG_FINAL = eg.FINAL_DECISION
EG_GATES = eg.REQUIRED_GATE_AUDIT
EG_QUEUE = eg.EH_QUEUE
EG_ATTRIBUTION = eg.SURVIVOR_ATTRIBUTION
EG_DIRECTION = eg.SURVIVOR_DIRECTION
EG_CURVE = eg.SURVIVOR_CURVE
EG_PACKAGE = eg.SURVIVOR_PACKAGE
EG_CONTROL = eg.SURVIVOR_CONTROL
EG_AXIS = eg.SOURCE_AXIS_SUMMARY
EG_TRADE_TAPE = eg.TRADE_TAPE

RUNTIME_MANIFEST = RUN_DIR / "survivor_runtime_probe_manifest.csv"
FEATURE_HANDOFF = RUN_DIR / "survivor_feature_handoff_manifest.csv"
PROXY_EXPECTED = RUN_DIR / "survivor_proxy_expected_contract.csv"
WATCH_POLICY = RUN_DIR / "survivor_watch_policy.csv"
BLOCKER_MATRIX = RUN_DIR / "runtime_probe_blocker_matrix.csv"
PACKAGE_INDEX = RUN_DIR / "runtime_probe_package_index.csv"
EI_QUEUE = RUN_DIR / "run337EI_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EG_FINAL,
    EG_GATES,
    EG_QUEUE,
    EG_ATTRIBUTION,
    EG_DIRECTION,
    EG_CURVE,
    EG_PACKAGE,
    EG_CONTROL,
    EG_AXIS,
    EG_TRADE_TAPE,
    ee.TRAINED_MODEL_MANIFEST,
    ee.ONNX_PARITY,
    ee.FEATURE_COMPATIBILITY,
    ee.FEATURE_SET_MATRIX,
    ee.SOURCE_MODEL_INPUT,
)
OUTPUT_FILES = (
    RUNTIME_MANIFEST,
    FEATURE_HANDOFF,
    PROXY_EXPECTED,
    WATCH_POLICY,
    BLOCKER_MATRIX,
    PACKAGE_INDEX,
    EI_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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

RUNTIME_COLUMNS = (
    "probe_id",
    "model_id",
    "proxy_rank",
    "onnx_path",
    "onnx_sha256",
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "class_order_json",
    "probability_output_name",
    "decision_policy",
    "threshold_policy",
    "proxy_expected_contract",
    "watch_policy",
    "execution_status",
    "allowed_claim",
    "forbidden_action",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
    "included_features_json",
    "source_model_input",
    "source_timestamp_start",
    "source_timestamp_end",
    "train_rows",
    "validation_rows",
    "oos_rows",
    "missing_count",
    "nonfinite_rows",
    "handoff_status",
    "claim_boundary",
)
EXPECTED_COLUMNS = (
    "model_id",
    "proxy_rank",
    "split",
    "expected_trade_rows",
    "expected_net_log_return_after_cost",
    "expected_profit_factor",
    "expected_max_drawdown",
    "expected_recovery_factor",
    "trade_tape_path",
    "trade_tape_sha256",
    "timestamp_basis",
    "comparison_tolerance",
    "required_runtime_outputs",
    "claim_boundary",
)
WATCH_COLUMNS = (
    "model_id",
    "proxy_rank",
    "density_watch_rows",
    "direction_watch_rows",
    "curve_watch_rows",
    "shifted_alignment_close_watch_rows",
    "watch_policy_status",
    "runtime_review_requirement",
    "claim_boundary",
)
BLOCKER_COLUMNS = (
    "blocker_id",
    "status",
    "applies_to",
    "blocked_action_or_claim",
    "required_before_release",
    "effect",
    "claim_boundary",
)
INDEX_COLUMNS = (
    "artifact_id",
    "artifact_path",
    "artifact_type",
    "rows_or_identity",
    "sha256",
    "package_role",
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
    return str(value).strip().lower() in {"1", "true", "yes", "passed"}


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def source_summary() -> dict[str, Any]:
    source = pd.read_parquet(io_path(ee.SOURCE_MODEL_INPUT), columns=["timestamp", "split"])
    timestamps = pd.to_datetime(source["timestamp"], utc=True)
    split_counts = source["split"].astype(str).value_counts().to_dict()
    return {
        "source_timestamp_start": str(timestamps.min()),
        "source_timestamp_end": str(timestamps.max()),
        "train_rows": int(split_counts.get("train", 0)),
        "validation_rows": int(split_counts.get("validation", 0)),
        "oos_rows": int(split_counts.get("oos", 0)),
    }


def build_runtime_manifest() -> list[dict[str, Any]]:
    packages = pd.read_csv(io_path(EG_PACKAGE))
    model_manifest = pd.read_csv(io_path(ee.TRAINED_MODEL_MANIFEST))
    manifest_by_model = {row["model_id"]: row for row in model_manifest.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for package in packages.sort_values("proxy_rank").to_dict("records"):
        model = manifest_by_model[package["model_id"]]
        rows.append(
            {
                "probe_id": f"eh_rank{as_int(package['proxy_rank']):02d}",
                "model_id": package["model_id"],
                "proxy_rank": as_int(package["proxy_rank"]),
                "onnx_path": model["onnx_path"],
                "onnx_sha256": model["onnx_sha256"],
                "feature_set_id": model["feature_set_id"],
                "feature_count": model["feature_count"],
                "feature_order_hash": model["feature_order_hash"],
                "class_order_json": model["class_order_json"],
                "probability_output_name": model["onnx_probability_output_name"],
                "decision_policy": "three_class_argmax_from_probabilities(3분류 확률 argmax)",
                "threshold_policy": "not_applicable_no_threshold_sweep(해당 없음, 임계값 탐색 없음)",
                "proxy_expected_contract": rel(PROXY_EXPECTED),
                "watch_policy": rel(WATCH_POLICY),
                "execution_status": "materialized_no_mt5_execution(물질화, MT5 실행 없음)",
                "allowed_claim": "runtime_input_review_only(런타임 입력 검토 전용)",
                "forbidden_action": "candidate selection, MT5 execution, Forward claim, live readiness(후보 선택/MT5 실행/전진 주장/라이브 준비 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_feature_handoff() -> list[dict[str, Any]]:
    runtime_manifest = pd.DataFrame(build_runtime_manifest())
    used_features = sorted(runtime_manifest["feature_set_id"].unique().tolist())
    feature_sets = pd.read_csv(io_path(ee.FEATURE_SET_MATRIX))
    compatibility = pd.read_csv(io_path(ee.FEATURE_COMPATIBILITY))
    source = source_summary()
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets.to_dict("records")}
    compat_by_id = {row["feature_set_id"]: row for row in compatibility.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for feature_set_id in used_features:
        feature = feature_by_id[feature_set_id]
        compat = compat_by_id[feature_set_id]
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "feature_count": feature["included_feature_count"],
                "feature_order_hash": feature["feature_order_hash"],
                "included_features_json": feature["included_features_json"],
                "source_model_input": rel(ee.SOURCE_MODEL_INPUT),
                "source_timestamp_start": source["source_timestamp_start"],
                "source_timestamp_end": source["source_timestamp_end"],
                "train_rows": source["train_rows"],
                "validation_rows": source["validation_rows"],
                "oos_rows": source["oos_rows"],
                "missing_count": compat["missing_count"],
                "nonfinite_rows": compat["nonfinite_rows"],
                "handoff_status": "feature_handoff_materialized_review_required(피처 인계 물질화, 검토 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_expected() -> list[dict[str, Any]]:
    attribution = pd.read_csv(io_path(EG_ATTRIBUTION))
    tape_hash = sha256_file(EG_TRADE_TAPE)
    rows: list[dict[str, Any]] = []
    for row in attribution.sort_values(["proxy_rank", "split"]).to_dict("records"):
        rows.append(
            {
                "model_id": row["model_id"],
                "proxy_rank": as_int(row["proxy_rank"]),
                "split": row["split"],
                "expected_trade_rows": as_int(row["trade_count"]),
                "expected_net_log_return_after_cost": as_float(row["net_log_return_after_cost"]),
                "expected_profit_factor": as_float(row["profit_factor"]),
                "expected_max_drawdown": as_float(row["max_drawdown"]),
                "expected_recovery_factor": as_float(row["recovery_factor"]),
                "trade_tape_path": rel(EG_TRADE_TAPE),
                "trade_tape_sha256": tape_hash,
                "timestamp_basis": "source_model_input_timestamp_utc(원천 모델 입력 UTC 시각)",
                "comparison_tolerance": "net_abs<=1e-9;pf_abs<=1e-9;trade_rows_exact(순손익/PF 허용오차, 거래수 정확 일치)",
                "required_runtime_outputs": "runtime_trade_tape.csv;runtime_probability_tape.csv;runtime_diff_summary.csv",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_watch_policy() -> list[dict[str, Any]]:
    attribution = pd.read_csv(io_path(EG_ATTRIBUTION))
    direction = pd.read_csv(io_path(EG_DIRECTION))
    curve = pd.read_csv(io_path(EG_CURVE))
    control = pd.read_csv(io_path(EG_CONTROL))
    models = sorted(attribution["model_id"].unique().tolist(), key=lambda model: int(attribution.loc[attribution["model_id"].eq(model), "proxy_rank"].iloc[0]))
    rows: list[dict[str, Any]] = []
    for model_id in models:
        rank = as_int(attribution.loc[attribution["model_id"].eq(model_id), "proxy_rank"].iloc[0])
        density_watch = int(attribution.loc[attribution["model_id"].eq(model_id), "attribution_status"].astype(str).str.contains("density_shift_watch").sum())
        direction_watch = int(direction.loc[direction["model_id"].eq(model_id), "direction_status"].astype(str).ne("direction_proxy_clear_review_only").sum())
        curve_watch = int(curve.loc[curve["model_id"].eq(model_id), "curve_review_status"].astype(str).eq("curve_watch_review_required").sum())
        shifted_watch = int(control.loc[control["model_id"].eq(model_id), "control_review_status"].astype(str).eq("shifted_alignment_close_watch").sum())
        watch_count = density_watch + direction_watch + curve_watch + shifted_watch
        rows.append(
            {
                "model_id": model_id,
                "proxy_rank": rank,
                "density_watch_rows": density_watch,
                "direction_watch_rows": direction_watch,
                "curve_watch_rows": curve_watch,
                "shifted_alignment_close_watch_rows": shifted_watch,
                "watch_policy_status": "runtime_probe_must_report_watch_rows" if watch_count else "runtime_probe_watch_clear",
                "runtime_review_requirement": "EI must review before any external MT5 execution(EI가 외부 MT5 실행 전에 검토해야 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_blockers() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "actual_mt5_execution_out_of_scope",
            "status": "active",
            "applies_to": "all_survivors",
            "blocked_action_or_claim": "MT5 execution and Strategy Tester result(MT5 실행과 전략 테스터 결과)",
            "required_before_release": "run337EI review then explicit external runtime packet(EI 검토 후 명시적 외부 런타임 작업)",
            "effect": "EH is materialization only, so it cannot become Forward evidence(EH는 물질화 전용이라 전진 근거가 될 수 없다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "adapter_argmax_contract_review_required",
            "status": "active",
            "applies_to": "all_survivors",
            "blocked_action_or_claim": "runtime authority from ONNX package(ONNX 패키지 기반 런타임 권위)",
            "required_before_release": "prove adapter can reproduce 3-class argmax probability contract(어댑터가 3분류 argmax 확률 계약을 재현함을 증명)",
            "effect": "prevents model-file existence from being mistaken for runtime parity(모델 파일 존재를 런타임 동등성으로 오해하지 않게 한다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "watch_policy_review_required",
            "status": "active",
            "applies_to": "all_survivors",
            "blocked_action_or_claim": "winner selection from proxy package(프록시 패키지 기반 승자 선택)",
            "required_before_release": "density/direction/curve watch rows must be carried into runtime review(밀도/방향/곡선 감시 행을 런타임 검토에 이월)",
            "effect": "prevents overfit proxy survivor promotion(과적합 프록시 생존 후보 승격을 막는다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "forward_decision_not_available",
            "status": "active",
            "applies_to": "all_survivors",
            "blocked_action_or_claim": "Forward Passed or Forward Failed(전진 통과 또는 전진 실패)",
            "required_before_release": "actual external forward/runtime evidence(실제 외부 전진/런타임 근거)",
            "effect": "keeps this packet as research materialization only(이번 작업을 연구 물질화로만 둔다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_package_index(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        if path.suffix.lower() == ".csv":
            row_count = len(read_csv(path))
        elif path.suffix.lower() == ".json":
            row_count = ";".join(sorted(read_json(path).keys()))
        else:
            row_count = path.suffix.lower().lstrip(".")
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_path": rel(path),
                "artifact_type": path.suffix.lstrip(".") or "file",
                "rows_or_identity": row_count,
                "sha256": sha256_file(path),
                "package_role": "runtime_probe_input_materialization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ei_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EI_review_runtime_probe_manifest",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review survivor runtime probe manifest and feature handoff(생존 후보 런타임 탐침 목록과 피처 인계 검토)",
            "required_inputs": f"{rel(RUNTIME_MANIFEST)};{rel(FEATURE_HANDOFF)};{rel(PROXY_EXPECTED)}",
            "required_outputs": "runtime_manifest_review.csv;feature_handoff_review.csv",
            "blocked_if_missing": "manifest, feature handoff, proxy expected contract(목록/피처 인계/프록시 예상 계약)",
            "forbidden_action": "no MT5 execution during EI review(EI 검토 중 MT5 실행 금지)",
            "effect": "checks whether the materialized package is internally executable(물질화 패키지가 내부적으로 실행 가능한지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EI_review_adapter_and_blockers",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review adapter argmax contract and active blockers(어댑터 argmax 계약과 활성 차단 검토)",
            "required_inputs": f"{rel(BLOCKER_MATRIX)};{rel(WATCH_POLICY)}",
            "required_outputs": "adapter_contract_review.csv;runtime_blocker_review.csv",
            "blocked_if_missing": "blocker matrix or watch policy(차단 행렬 또는 감시 정책)",
            "forbidden_action": "no runtime authority claim(런타임 권위 주장 금지)",
            "effect": "decides whether the next packet can attempt external MT5 or must repair adapter handoff(다음 작업이 외부 MT5를 시도할지 어댑터 인계를 수리할지 결정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "EG 입력이 있어야 EH 물질화가 닫힌다."),
        ("parent_eg_gates_passed", final["eg_failed_gate_rows"] == 0, str(final["eg_failed_gate_rows"]), "0", "부모 EG 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["eg_next_action"] == RUN_ID, str(final["eg_next_action"]), RUN_ID, "라우팅이 EH로 정확히 이어졌는지 확인한다."),
        ("runtime_manifest_rows", final["runtime_manifest_rows"] == 7, str(final["runtime_manifest_rows"]), "7", "7개 생존 후보가 모두 런타임 입력으로 물질화되어야 한다."),
        ("feature_handoff_rows", final["feature_handoff_rows"] == 2, str(final["feature_handoff_rows"]), "2", "사용된 피처 묶음 2개가 인계 목록에 있어야 한다."),
        ("proxy_expected_rows", final["proxy_expected_rows"] == 21, str(final["proxy_expected_rows"]), "21", "7개 후보 x 3개 split 예상 계약이 있어야 한다."),
        ("blockers_active", final["active_blocker_rows"] == 4, str(final["active_blocker_rows"]), "4", "MT5/어댑터/감시/전진 차단이 명시되어야 한다."),
        ("ei_queue_materialized", final["ei_queue_rows"] == 2, str(final["ei_queue_rows"]), "2", "EI 검토 대기열이 있어야 한다."),
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
        "sample_scope": f"runtime_manifest_rows={final['runtime_manifest_rows']};proxy_expected_rows={final['proxy_expected_rows']}",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "materialized_runtime_inputs_review_required(런타임 입력 물질화 완료, 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "seven proxy survivor ONNX artifacts(7개 프록시 생존 후보 ONNX 산출물)",
        "decision_policy": "three_class_argmax_from_probabilities(3분류 확률 argmax)",
        "threshold_policy": "not_applicable_no_threshold_tuning(해당 없음, 임계값 조정 없음)",
        "selection_metric": "none, all survivors carried as review set(없음, 전체 생존 후보 검토 묶음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "expected_contract_rows": final["proxy_expected_rows"],
        "watch_policy_rows": final["watch_policy_rows"],
        "active_blocker_rows": final["active_blocker_rows"],
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_claim": "not_run_no_MT5(미실행, MT5 없음)",
        "package_status": "materialized_for_review(검토용 물질화)",
        "adapter_review_required": "three_class_argmax_contract(3분류 argmax 계약)",
        "runtime_authority": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "runtime manifest, feature handoff, proxy expected contract, blockers(런타임 목록/피처 인계/프록시 예상 계약/차단)",
        "evidence_missing": "EI review and external MT5 execution(EI 검토와 외부 MT5 실행)",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
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
    text = f"""# Stage337 run337EH Runtime Probe Input Materialization(런타임 탐침 입력 물질화)

## Conclusion(결론)

run337EH(337EH 실행)는 7개 proxy survivor(프록시 생존 후보)를 runtime probe input package(런타임 탐침 입력 패키지)로 물질화했다. 모델/ONNX(온엑스), feature handoff(피처 인계), proxy expected contract(프록시 예상 계약), watch policy(감시 정책), blocker matrix(차단 행렬)를 만들었다.

Action(행동): 실제 MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표)은 실행하지 않았다.

Effect(효과): 다음 run337EI(337EI 실행)는 이 패키지가 어댑터와 외부 런타임으로 넘어갈 수 있는지 검토한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- runtime_manifest_rows(런타임 목록 행): `{final["runtime_manifest_rows"]}`
- feature_handoff_rows(피처 인계 행): `{final["feature_handoff_rows"]}`
- proxy_expected_rows(프록시 예상 계약 행): `{final["proxy_expected_rows"]}`
- watch_policy_rows(감시 정책 행): `{final["watch_policy_rows"]}`
- active_blocker_rows(활성 차단 행): `{final["active_blocker_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EH

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 7개 프록시 생존 후보를 런타임 탐침 입력 패키지로 만들었지만 실제 MT5/Forward(전진)는 실행하지 않았다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(RUNTIME_MANIFEST)}`, `{rel(PROXY_EXPECTED)}`, `{rel(BLOCKER_MATRIX)}`
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
        f"  Stage337 run337EH focus complete: runtime probe input materialization(런타임 탐침 입력 물질화)에서 "
        f"runtime manifest(런타임 목록) `{final['runtime_manifest_rows']}`행, proxy expected contract(프록시 예상 계약) `{final['proxy_expected_rows']}`행을 만들었다. "
        "Effect(효과): 다음 run337EI에서 어댑터/차단/외부 MT5 가능성을 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EH focus complete")
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
## Stage337 run337EH(337EH 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 프록시 생존 후보 7개를 런타임 탐침 입력 패키지로 물질화했다. 실제 MT5/Forward/Goal(실제 MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EG("
    if "## Stage337 run337EH(337EH 실행)" not in current_text:
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
- runtime_manifest_rows(런타임 목록 행): `{final["runtime_manifest_rows"]}`
- active_blocker_rows(활성 차단 행): `{final["active_blocker_rows"]}`
- actual_mt5_execution(실제 MT5 실행): `not_run_eh_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy survivor runtime input review(프록시 생존 후보 런타임 입력 검토)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EH(337EH 실행) materialized proxy survivor runtime probe inputs(프록시 생존 후보 런타임 탐침 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)는 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EH(337EH 실행) materialized proxy survivor"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EH materialized runtime probe inputs for 7 proxy survivors and opened `{NEXT_RUN_ID}` without MT5/Forward claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EH materialized runtime probe inputs"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_survivor_runtime_probe_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"manifest_rows={final['runtime_manifest_rows']};proxy_expected_rows={final['proxy_expected_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "runtime_parity_artifact_lineage_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_no_mt5_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "runtime_probe_input_package",
        "scoreboard_lane": "runtime_parity_artifact_lineage",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_manifest_rows={final['runtime_manifest_rows']};proxy_expected_rows={final['proxy_expected_rows']}",
        "guardrail_kpi": "actual_mt5_not_run;no_selection;no_forward;active_blockers",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_artifact_lineage_model_validation",
        "evidence_scope": "EG proxy survivor runtime inputs materialized",
        "kpi_scope": "runtime_probe_input_package",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__runtime_input_materialization",
        "family": "runtime_parity_artifact_lineage_model_validation",
        "question": "can proxy survivor artifacts be materialized into runtime probe inputs",
        "metric_scope": "manifest_feature_handoff_expected_contract_blockers",
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
    runtime_rows = build_runtime_manifest()
    feature_rows = build_feature_handoff()
    expected_rows = build_proxy_expected()
    watch_rows = build_watch_policy()
    blocker_rows = build_blockers()
    queue_rows = build_ei_queue()
    artifacts: list[Path] = [
        write_csv(RUNTIME_MANIFEST, RUNTIME_COLUMNS, runtime_rows),
        write_csv(FEATURE_HANDOFF, FEATURE_COLUMNS, feature_rows),
        write_csv(PROXY_EXPECTED, EXPECTED_COLUMNS, expected_rows),
        write_csv(WATCH_POLICY, WATCH_COLUMNS, watch_rows),
        write_csv(BLOCKER_MATRIX, BLOCKER_COLUMNS, blocker_rows),
        write_csv(EI_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    artifacts.append(write_csv(PACKAGE_INDEX, INDEX_COLUMNS, build_package_index(artifacts)))
    eg_final = read_json(EG_FINAL)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "eg_next_action": eg_final.get("next_action", ""),
        "eg_failed_gate_rows": sum(1 for row in read_csv(EG_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "runtime_manifest_rows": len(runtime_rows),
        "feature_handoff_rows": len(feature_rows),
        "proxy_expected_rows": len(expected_rows),
        "watch_policy_rows": len(watch_rows),
        "active_blocker_rows": sum(1 for row in blocker_rows if row["status"] == "active"),
        "ei_queue_rows": len(queue_rows),
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
                "runtime_manifest_rows": final["runtime_manifest_rows"],
                "feature_handoff_rows": final["feature_handoff_rows"],
                "proxy_expected_rows": final["proxy_expected_rows"],
                "active_blocker_rows": final["active_blocker_rows"],
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
