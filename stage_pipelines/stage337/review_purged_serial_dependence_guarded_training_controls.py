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

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CP"
RUN_ID = "run337CP_review_purged_serial_dependence_guarded_training_controls_without_db_v1"
PARENT_RUN_ID = "run337CO_train_purged_serial_dependence_guarded_candidates_without_db_v1"
NEXT_RUN_ID = "run337CQ_design_weak_density_and_control_alignment_repair_without_db_v1"
STATUS = "completed_stage337CP_control_review_all_mt5_probe_held_weak_or_blocked_no_selection"
JUDGMENT = "purged_training_control_review_blocks_mt5_probe_all_models_weak_or_negative_control_blocked"
DECISION = "stage337CP_open_run337CQ_weak_density_and_control_alignment_repair_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CP_purged_guarded_training_control_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CP_purged_guarded_training_control_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CP_purged_guarded_training_control_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CO_DIR = STAGE_DIR / "02_runs" / "run337CO"
CO_FINAL = CO_DIR / "final_decision.json"
CO_GATES = CO_DIR / "required_gate_coverage_audit.csv"
CO_MODEL_MANIFEST = CO_DIR / "purged_trained_model_manifest.csv"
CO_SCORECARD = CO_DIR / "purged_guarded_model_scorecard.csv"
CO_PARITY = CO_DIR / "onnxruntime_parity_matrix.csv"
CO_CONTROLS = CO_DIR / "nonoverlap_control_scorecard.csv"
CO_RUNTIME = CO_DIR / "runtime_probe_disposition.csv"
CO_THRESHOLD_POLICY = CO_DIR / "decision_threshold_policy.csv"
CO_FEATURE_COMPATIBILITY = CO_DIR / "feature_input_compatibility.csv"

MODEL_REVIEW = RUN_DIR / "model_control_review_matrix.csv"
BLOCKED_ATTRIBUTION = RUN_DIR / "blocked_control_attribution.csv"
REVIEW_READY_WEAKNESS = RUN_DIR / "review_ready_weakness_matrix.csv"
MT5_DISPOSITION_REVIEW = RUN_DIR / "mt5_probe_disposition_review.csv"
NEXT_QUEUE = RUN_DIR / "run337CQ_repair_design_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CO_FINAL,
    CO_GATES,
    CO_MODEL_MANIFEST,
    CO_SCORECARD,
    CO_PARITY,
    CO_CONTROLS,
    CO_RUNTIME,
    CO_THRESHOLD_POLICY,
    CO_FEATURE_COMPATIBILITY,
)
OUTPUT_FILES = (
    MODEL_REVIEW,
    BLOCKED_ATTRIBUTION,
    REVIEW_READY_WEAKNESS,
    MT5_DISPOSITION_REVIEW,
    NEXT_QUEUE,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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

MODEL_REVIEW_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
    "validation_balanced_accuracy",
    "oos_balanced_accuracy",
    "validation_signal_density",
    "oos_signal_density",
    "blocking_controls",
    "passed_controls",
    "runtime_input_disposition",
    "review_status",
    "review_reason",
    "claim_boundary",
)
BLOCKED_COLUMNS = (
    "control_id",
    "blocked_rows",
    "blocked_models",
    "avg_oos_control_balanced_accuracy",
    "avg_oos_actual_balanced_accuracy",
    "avg_oos_control_minus_actual",
    "interpretation",
    "claim_boundary",
)
WEAKNESS_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
    "validation_balanced_accuracy",
    "oos_balanced_accuracy",
    "validation_signal_density",
    "oos_signal_density",
    "weakness_reason",
    "mt5_probe_disposition",
    "claim_boundary",
)
MT5_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "co_disposition",
    "cp_disposition",
    "blocking_controls",
    "weakness_reason",
    "next_condition",
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

MIN_VALIDATION_BALANCED = 0.38
MIN_OOS_BALANCED = 0.40
MIN_SIGNAL_DENSITY = 0.03


def fnum(value: Any, default: float = 0.0) -> float:
    if value is None or value == "" or pd.isna(value):
        return default
    return float(value)


def status_reason(
    blocking_controls: Sequence[str],
    validation_balanced: float,
    oos_balanced: float,
    validation_density: float,
    oos_density: float,
) -> tuple[str, str, str]:
    if blocking_controls:
        return (
            "mt5_probe_held_negative_control_blocked",
            ";".join(blocking_controls),
            "negative controls(부정 대조)가 아직 실제 신호와 분리되지 않았다.",
        )
    weakness: list[str] = []
    if validation_balanced < MIN_VALIDATION_BALANCED:
        weakness.append(f"validation_balanced<{MIN_VALIDATION_BALANCED:.2f}")
    if oos_balanced < MIN_OOS_BALANCED:
        weakness.append(f"oos_balanced<{MIN_OOS_BALANCED:.2f}")
    if validation_density < MIN_SIGNAL_DENSITY or oos_density < MIN_SIGNAL_DENSITY:
        weakness.append(f"signal_density<{MIN_SIGNAL_DENSITY:.2f}")
    if weakness:
        return (
            "mt5_probe_held_control_passed_but_weak_signal",
            ";".join(weakness),
            "controls(대조)는 약해졌지만 actual signal(실제 신호)이 약하거나 너무 희소하다.",
        )
    return (
        "mt5_probe_review_candidate_no_forward_claim",
        "none",
        "control and signal floors(대조와 신호 하한)을 통과했지만 아직 선택이나 MT5 실행은 아니다.",
    )


def build_review() -> dict[str, Any]:
    co_final = read_json(CO_FINAL)
    models = pd.read_csv(io_path(CO_MODEL_MANIFEST))
    scores = pd.read_csv(io_path(CO_SCORECARD))
    controls = pd.read_csv(io_path(CO_CONTROLS))
    runtime = pd.read_csv(io_path(CO_RUNTIME))

    score_lookup: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row in scores.to_dict("records"):
        score_lookup[(row["model_id"], row["split"])] = row
    runtime_lookup = {row["model_id"]: row for row in runtime.to_dict("records")}
    blocking_lookup: dict[str, list[str]] = {}
    passed_lookup: dict[str, list[str]] = {}
    for row in controls.to_dict("records"):
        if str(row.get("blocks_runtime_probe", "")).lower() == "true":
            blocking_lookup.setdefault(row["model_id"], []).append(row["control_id"])
        else:
            passed_lookup.setdefault(row["model_id"], []).append(row["control_id"])

    review_rows: list[dict[str, Any]] = []
    weakness_rows: list[dict[str, Any]] = []
    mt5_rows: list[dict[str, Any]] = []
    for model in models.to_dict("records"):
        model_id = model["model_id"]
        validation = score_lookup[(model_id, "validation")]
        oos = score_lookup[(model_id, "oos")]
        blocking = sorted(set(blocking_lookup.get(model_id, [])))
        status, reason_code, reason_text = status_reason(
            blocking,
            fnum(validation["balanced_accuracy"]),
            fnum(oos["balanced_accuracy"]),
            fnum(validation["signal_density"]),
            fnum(oos["signal_density"]),
        )
        review_row = {
            "model_id": model_id,
            "label_candidate_id": model["label_candidate_id"],
            "contract_id": model["contract_id"],
            "model_family": model["model_family"],
            "validation_balanced_accuracy": fnum(validation["balanced_accuracy"]),
            "oos_balanced_accuracy": fnum(oos["balanced_accuracy"]),
            "validation_signal_density": fnum(validation["signal_density"]),
            "oos_signal_density": fnum(oos["signal_density"]),
            "blocking_controls": ";".join(blocking),
            "passed_controls": ";".join(sorted(set(passed_lookup.get(model_id, [])))),
            "runtime_input_disposition": runtime_lookup[model_id]["mt5_probe_disposition"],
            "review_status": status,
            "review_reason": reason_text,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        review_rows.append(review_row)
        if status == "mt5_probe_held_control_passed_but_weak_signal":
            weakness_rows.append(
                {
                    "model_id": model_id,
                    "label_candidate_id": model["label_candidate_id"],
                    "contract_id": model["contract_id"],
                    "model_family": model["model_family"],
                    "validation_balanced_accuracy": fnum(validation["balanced_accuracy"]),
                    "oos_balanced_accuracy": fnum(oos["balanced_accuracy"]),
                    "validation_signal_density": fnum(validation["signal_density"]),
                    "oos_signal_density": fnum(oos["signal_density"]),
                    "weakness_reason": reason_code,
                    "mt5_probe_disposition": status,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        mt5_rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": model["label_candidate_id"],
                "contract_id": model["contract_id"],
                "co_disposition": runtime_lookup[model_id]["mt5_probe_disposition"],
                "cp_disposition": status,
                "blocking_controls": ";".join(blocking),
                "weakness_reason": reason_code if not blocking else "",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    blocked = controls[controls["blocks_runtime_probe"].astype(str).str.lower() == "true"].copy()
    blocked_rows: list[dict[str, Any]] = []
    for control_id, group in blocked.groupby("control_id", sort=True):
        interpretation = "control alignment blocks MT5 probe(대조 정렬이 MT5 탐침을 막음)"
        if control_id == "day_block_permutation_control":
            interpretation = "day block permutation(일 단위 블록 순열)이 너무 실제와 비슷해 calendar carry(달력 이월) 위험이 남음"
        elif control_id.startswith("label_shift"):
            interpretation = "shifted label control(이동 라벨 대조)이 충분히 약해지지 않아 serial dependence(연속 의존) 위험이 남음"
        elif control_id == "purged_adjacent_split_control":
            interpretation = "shift controls(이동 대조)가 통과하지 않아 purged adjacent split(제거 인접 분할)도 보류"
        blocked_rows.append(
            {
                "control_id": control_id,
                "blocked_rows": int(group.shape[0]),
                "blocked_models": int(group["model_id"].nunique()),
                "avg_oos_control_balanced_accuracy": float(group["oos_control_balanced_accuracy"].fillna(0).mean()),
                "avg_oos_actual_balanced_accuracy": float(group["oos_actual_balanced_accuracy"].fillna(0).mean()),
                "avg_oos_control_minus_actual": float(group["oos_control_minus_actual"].fillna(0).mean()),
                "interpretation": interpretation,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    queue_rows = [
        {
            "queue_id": "run337CQ_day_block_alignment_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "day block alignment(일 단위 블록 정렬) 원인을 feature/session/regime slice(피처/세션/레짐 조각)로 분해",
            "required_inputs": rel(BLOCKED_ATTRIBUTION),
            "required_outputs": "day_block_alignment_repair_design.csv",
            "forbidden_action": "do not drop profitable days or tune filters from OOS(OOS에서 수익일 제거/필터 튜닝 금지)",
            "effect": "calendar carry(달력 이월)가 모델 신호처럼 보이는지 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CQ_shift_residual_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "label shift residual(라벨 이동 잔차)을 horizon/feature state carry(기간/피처 상태 이월)로 분해",
            "required_inputs": rel(CO_CONTROLS),
            "required_outputs": "shift_residual_repair_design.csv",
            "forbidden_action": "do not pick purge gap by profit(수익으로 제거 간격 선택 금지)",
            "effect": "serial dependence(연속 의존) 위험이 남은 축을 다음 설계로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CQ_volnorm_low_density_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "control-passed volnorm models(대조 통과 변동성 정규화 모델)의 weak/sparse signal(약하고 희소한 신호)을 재검토",
            "required_inputs": rel(REVIEW_READY_WEAKNESS),
            "required_outputs": "weak_density_repair_design.csv",
            "forbidden_action": "do not lower thresholds to create trades(거래를 만들려고 임계값 낮추기 금지)",
            "effect": "대조 통과가 실제 사용성으로 과장되지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CQ_mt5_probe_deferred",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "MT5 probe(MT5 탐침)는 control and signal floor(대조와 신호 하한)가 모두 통과할 때까지 보류",
            "required_inputs": rel(MT5_DISPOSITION_REVIEW),
            "required_outputs": "no_mt5_probe_release_until_repair_review.md",
            "forbidden_action": "do not create MT5 package from weak/control-blocked models(약하거나 대조 차단 모델로 MT5 패키지 생성 금지)",
            "effect": "runtime work(런타임 작업)를 대조 실패의 우회로로 쓰지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return {
        "co_final": co_final,
        "review_rows": review_rows,
        "blocked_rows": blocked_rows,
        "weakness_rows": weakness_rows,
        "mt5_rows": mt5_rows,
        "queue_rows": queue_rows,
    }


def build_gates(result: Mapping[str, Any], final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("cp_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CO evidence(CO 근거)를 연결했다."),
        row("cp_gate_parent_points_to_cp", result["co_final"].get("next_action", "") == RUN_ID, result["co_final"].get("next_action", ""), RUN_ID, "CO next_action(다음 행동)과 CP run(실행)이 맞는다."),
        row("cp_gate_review_rows", final["review_rows"] == 40, final["review_rows"], "40", "모든 CO model(모델)을 검토했다."),
        row("cp_gate_blocked_attribution", final["blocked_attribution_rows"] >= 1, final["blocked_attribution_rows"], ">=1", "blocking controls(차단 대조)를 원인별로 묶었다."),
        row("cp_gate_weakness_rows", final["weakness_rows"] == 4, final["weakness_rows"], "4", "대조 통과 4개도 weak/sparse signal(약하고 희소한 신호)로 표시했다."),
        row("cp_gate_mt5_release_none", final["mt5_release_rows"] == 0, final["mt5_release_rows"], "0", "MT5 probe(MT5 탐침)로 넘길 모델이 없음을 명시했다."),
        row("cp_gate_next_queue", final["next_queue_rows"] >= 3, final["next_queue_rows"], ">=3", "다음 repair design(수리 설계) 대기열을 만들었다."),
        row("cp_gate_no_new_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CP는 review(검토)만 수행한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "CO trained diagnostic models(CO 진단 학습 모델) review only",
        "target_and_label": "purged guarded candidate labels(제거 방어 후보 라벨)",
        "split_method": "CO purged/embargo splits(CO 제거/격리 분할)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "control blocks(대조 차단), weak signal floors(약한 신호 하한), runtime disposition(런타임 처분)",
        "threshold_policy": "unchanged and not tuned(변경 없음, 조정 없음)",
        "overfit_risk": "promoting control-passed weak model as usable(대조 통과 약한 모델을 사용 가능으로 과장)",
        "calibration_risk": "scores remain diagnostic(점수는 진단용)",
        "comparison_baseline": "CO model scorecard and controls(CO 점수표와 대조)",
        "validation_judgment": "mt5_probe_held_all_models(전체 MT5 탐침 보류)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "CO timestamp outputs reviewed; no new rows(새 행 없음)",
        "sample_scope": "CO review artifacts only(CO 검토 산출물만)",
        "missing_or_duplicate_check": "row counts checked by gates(행 수는 게이트로 확인)",
        "feature_label_boundary": "no relabeling/no new features(재라벨/새 피처 없음)",
        "split_boundary": "CO effective split review(CO 유효 분할 검토)",
        "leakage_risk": "using review-ready rows as selected candidates(검토 가능 행을 선택 후보로 과장)",
        "data_hash_or_identity": {"co_final_sha256": sha256_file(CO_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "MT5 probe disposition review(MT5 탐침 처분 검토)",
        "mt5_runtime_probe": "not_run",
        "release_rows": final["mt5_release_rows"],
        "held_rows": final["mt5_held_rows"],
        "usable_for": "repair design(수리 설계)",
        "not_usable_for": "runtime authority(런타임 권위), Forward Passed(전진 통과)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "model review matrix(모델 검토 행렬), blocked attribution(차단 귀속), weakness matrix(약점 행렬), MT5 disposition review(MT5 처분 검토)",
        "evidence_missing": "new repair design(CQ 수리 설계), new training(새 학습), MT5 runtime probe(MT5 런타임 탐침)",
        "judgment_label": "exploratory_blocked_for_mt5(탐색, MT5 차단)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "대조를 통과한 4개도 약하고 희소해서 MT5로 보내지 않는다.",
    }
    receipt_paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CP Purged Guarded Training Control Review(제거 방어 학습 대조 검토)

## Conclusion(결론)

run337CP(337CP 실행)는 CO trained models(CO 학습 모델) `40`개를 control review(대조 검토)로 닫았다. `36`개는 negative control(부정 대조)로 MT5 probe(MT5 탐침)를 보류했고, control-passed(대조 통과) `4`개도 validation/OOS balanced accuracy(검증/실외표본 균형 정확도)와 signal density(신호 밀도)가 약해 MT5로 넘기지 않는다.

Effect(효과): 다음 run337CQ(337CQ 실행)는 MT5 package(MT5 패키지)가 아니라 weak density/control alignment repair design(약한 밀도/대조 정렬 수리 설계)이다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- review_rows(검토 행): `{final["review_rows"]}`
- negative_control_held_rows(부정 대조 보류 행): `{final["negative_control_held_rows"]}`
- weakness_rows(약점 행): `{final["weakness_rows"]}`
- mt5_release_rows(MT5 해제 행): `{final["mt5_release_rows"]}`
- next_queue_rows(다음 대기열 행): `{final["next_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- new_training(새 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CP

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): CO 모델 전체를 MT5 probe(MT5 탐침)에서 보류하고 CQ repair design(CQ 수리 설계)을 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(MODEL_REVIEW)}`, `{rel(MT5_DISPOSITION_REVIEW)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- mt5_release_rows(MT5 해제 행): `{final["mt5_release_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CP focus complete: purged guarded training control review(제거 방어 학습 대조 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): 모든 MT5 probe(MT5 탐침)를 보류하고 weak density/control alignment repair design(약한 밀도/대조 정렬 수리 설계)을 연다."
    )
    if "Stage337 run337CP focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CP focus complete:.*?(?=\n- >-\n  Stage337 run337CO|\n[A-Za-z0-9_]+:)",
            focus_entry,
            workspace_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
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
## Stage337 run337CP(337CP 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CO 모델 `40`개를 검토했고 MT5 probe(MT5 탐침)는 모두 보류했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CP\(337CP 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CO|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CO(337CO"
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
- actual_mt5_execution(실제 MT5 실행): `held_all_models_after_cp_review`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 weak density/control alignment repair design(약한 밀도/대조 정렬 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CP(337CP 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CP(337CP 실행) reviewed purged guarded controls(제거 방어 대조). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CP reviewed purged guarded controls" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CP reviewed purged guarded controls(제거 방어 대조) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "purged_guarded_training_control_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"review_rows={final['review_rows']};mt5_release_rows={final['mt5_release_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__control_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "control_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "control_review",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "review_no_training_no_selection",
        "scoreboard_lane": "model_validation_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"mt5_release_rows={final['mt5_release_rows']};weakness_rows={final['weakness_rows']};negative_control_held_rows={final['negative_control_held_rows']}",
        "guardrail_kpi": "no_mt5_probe;no_selection;no_threshold_tuning",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__control_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_result_judgment_artifact_lineage",
        "evidence_scope": "CO controls reviewed for MT5 disposition",
        "kpi_scope": "review_no_training_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};mt5_release_rows={final['mt5_release_rows']};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__control_review",
        "family": "model_validation_result_judgment_artifact_lineage",
        "question": "should any CO purged guarded model proceed to MT5 probe",
        "metric_scope": "control_review_mt5_disposition_weakness",
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
    result = build_review()
    mt5_release_rows = [
        row for row in result["mt5_rows"] if row["cp_disposition"] == "mt5_probe_review_candidate_no_forward_claim"
    ]
    negative_control_held = [
        row for row in result["review_rows"] if row["review_status"] == "mt5_probe_held_negative_control_blocked"
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "review_rows": len(result["review_rows"]),
        "negative_control_held_rows": len(negative_control_held),
        "blocked_attribution_rows": len(result["blocked_rows"]),
        "weakness_rows": len(result["weakness_rows"]),
        "mt5_disposition_rows": len(result["mt5_rows"]),
        "mt5_held_rows": len(result["mt5_rows"]) - len(mt5_release_rows),
        "mt5_release_rows": len(mt5_release_rows),
        "next_queue_rows": len(result["queue_rows"]),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(result, final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts: list[Path] = [
        write_csv(MODEL_REVIEW, MODEL_REVIEW_COLUMNS, result["review_rows"]),
        write_csv(BLOCKED_ATTRIBUTION, BLOCKED_COLUMNS, result["blocked_rows"]),
        write_csv(REVIEW_READY_WEAKNESS, WEAKNESS_COLUMNS, result["weakness_rows"]),
        write_csv(MT5_DISPOSITION_REVIEW, MT5_COLUMNS, result["mt5_rows"]),
        write_csv(NEXT_QUEUE, QUEUE_COLUMNS, result["queue_rows"]),
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
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
