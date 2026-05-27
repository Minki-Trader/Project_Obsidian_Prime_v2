from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
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
    now_utc,
)
from stage_pipelines.stage337.train_guarded_directional_label_action_candidates import (  # noqa: E402
    CANDIDATE_INPUT_MANIFEST,
    LABEL_CANDIDATE_MATRIX,
    SOURCE_MODEL_INPUT,
    label_values,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CM"
RUN_ID = "run337CM_design_serial_dependence_label_boundary_repair_without_db_v1"
PARENT_RUN_ID = "run337CL_review_guarded_directional_label_action_candidate_training_without_db_v1"
NEXT_RUN_ID = "run337CN_materialize_serial_dependence_label_boundary_repair_inputs_without_db_v1"
STATUS = "completed_stage337CM_serial_dependence_label_boundary_repair_design_materialized_no_training_no_selection"
JUDGMENT = "serial_dependence_repair_design_required_before_training_or_mt5_probe"
DECISION = "stage337CM_open_run337CN_materialize_serial_dependence_label_boundary_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CM_serial_dependence_label_boundary_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CM_serial_dependence_label_boundary_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CM_serial_dependence_label_boundary_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CL_DIR = STAGE_DIR / "02_runs" / "run337CL"
CL_FINAL = CL_DIR / "final_decision.json"
CL_NEGATIVE_ATTRIBUTION = CL_DIR / "negative_control_attribution_matrix.csv"
CL_RUNTIME_DISPOSITION = CL_DIR / "runtime_probe_disposition.csv"
CL_REPAIR_QUEUE = CL_DIR / "run337CM_repair_design_queue.csv"

LABEL_AUTOCORR = RUN_DIR / "label_autocorrelation_and_shift_gap_matrix.csv"
RETURN_AUTOCORR = RUN_DIR / "future_return_autocorrelation_matrix.csv"
PURGED_SPLIT_CONTRACT = RUN_DIR / "purged_embargo_split_contract_candidate.csv"
NONOVERLAP_CONTROL_PLAN = RUN_DIR / "nonoverlap_horizon_negative_control_plan.csv"
DIRECTION_FLIP_ATTRIBUTION = RUN_DIR / "direction_flip_attribution_matrix.csv"
REPAIR_DECISION_MATRIX = RUN_DIR / "repair_design_decision_matrix.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CL_FINAL,
    CL_NEGATIVE_ATTRIBUTION,
    CL_RUNTIME_DISPOSITION,
    CL_REPAIR_QUEUE,
    SOURCE_MODEL_INPUT,
    LABEL_CANDIDATE_MATRIX,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    LABEL_AUTOCORR,
    RETURN_AUTOCORR,
    PURGED_SPLIT_CONTRACT,
    NONOVERLAP_CONTROL_PLAN,
    DIRECTION_FLIP_ATTRIBUTION,
    REPAIR_DECISION_MATRIX,
    REQUIRED_GATE_AUDIT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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

LAGS = (1, 2, 3, 6, 12, 18, 24, 36, 48, 72)
LABEL_COLUMNS = (
    "label_candidate_id",
    "split",
    "lag_bars",
    "rows",
    "same_class_rate",
    "balanced_accuracy_y_t_vs_y_t_minus_lag",
    "nonflat_direction_agreement_rate",
    "risk_read",
    "claim_boundary",
)
RETURN_COLUMNS = (
    "split",
    "lag_bars",
    "rows",
    "future_return_autocorrelation",
    "abs_autocorrelation",
    "risk_read",
    "claim_boundary",
)
PURGE_COLUMNS = (
    "contract_id",
    "purge_gap_bars",
    "embargo_bars",
    "intended_use",
    "blocks_if",
    "forbidden_action",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "control_id",
    "priority",
    "shift_or_block",
    "hypothesis",
    "required_metric",
    "pass_condition",
    "forbidden_action",
    "claim_boundary",
)
DIRECTION_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "validation_control_balanced_accuracy",
    "oos_control_balanced_accuracy",
    "oos_actual_balanced_accuracy",
    "interpretation",
    "repair_use",
    "claim_boundary",
)
DECISION_COLUMNS = (
    "decision_id",
    "status",
    "reason",
    "next_action",
    "forbidden_action",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fnum(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def read_source_frame() -> pd.DataFrame:
    return pd.read_parquet(io_path(SOURCE_MODEL_INPUT))


def finite_corr(a: np.ndarray, b: np.ndarray) -> float:
    mask = np.isfinite(a) & np.isfinite(b)
    if int(mask.sum()) < 3:
        return 0.0
    av = a[mask]
    bv = b[mask]
    if float(np.std(av)) == 0.0 or float(np.std(bv)) == 0.0:
        return 0.0
    return float(np.corrcoef(av, bv)[0, 1])


def build_label_autocorr(df: pd.DataFrame, candidates: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    split_values = df["split"].astype(str)
    for candidate in candidates:
        y_all = label_values(df, candidate)
        candidate_id = candidate["candidate_id"]
        for split in ("train", "validation", "oos"):
            y = y_all[split_values.eq(split).to_numpy()]
            for lag in LAGS:
                if len(y) <= lag:
                    continue
                current = y[lag:]
                prior = y[:-lag]
                same_rate = float(np.mean(current == prior))
                bal = float(balanced_accuracy_score(current, prior))
                direction_mask = (current != 1) & (prior != 1)
                if int(direction_mask.sum()) == 0:
                    nonflat_agreement = 0.0
                else:
                    nonflat_agreement = float(np.mean(np.sign(current[direction_mask] - 1) == np.sign(prior[direction_mask] - 1)))
                risk_read = "serial_memory_watch"
                if lag == 12 and bal >= 0.45:
                    risk_read = "horizon_shift_memory_high"
                elif bal >= 0.50:
                    risk_read = "serial_memory_high"
                rows.append(
                    {
                        "label_candidate_id": candidate_id,
                        "split": split,
                        "lag_bars": lag,
                        "rows": int(len(current)),
                        "same_class_rate": same_rate,
                        "balanced_accuracy_y_t_vs_y_t_minus_lag": bal,
                        "nonflat_direction_agreement_rate": nonflat_agreement,
                        "risk_read": risk_read,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def build_return_autocorr(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    split_values = df["split"].astype(str)
    for split in ("train", "validation", "oos"):
        values = df.loc[split_values.eq(split), "future_log_return_12"].astype(float).to_numpy()
        for lag in LAGS:
            if len(values) <= lag:
                continue
            corr = finite_corr(values[lag:], values[:-lag])
            risk_read = "return_memory_watch"
            if lag == 12 and abs(corr) >= 0.05:
                risk_read = "horizon_return_memory_detected"
            rows.append(
                {
                    "split": split,
                    "lag_bars": lag,
                    "rows": int(len(values) - lag),
                    "future_return_autocorrelation": corr,
                    "abs_autocorrelation": abs(corr),
                    "risk_read": risk_read,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_purged_contracts() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for gap in (12, 24, 48, 72):
        rows.append(
            {
                "contract_id": f"purged_embargo_gap{gap}",
                "purge_gap_bars": str(gap),
                "embargo_bars": str(gap),
                "intended_use": "candidate split stress only(후보 분할 압박 전용)",
                "blocks_if": "shifted_return_control remains high after purge(제거 후에도 이동 수익률 대조가 높음)",
                "forbidden_action": "do not choose purge gap from profit(수익으로 제거 간격 선택 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_nonoverlap_controls() -> list[dict[str, str]]:
    return [
        {
            "control_id": "label_shift_gap24_control",
            "priority": "P0",
            "shift_or_block": "24 bars",
            "hypothesis": "edge should weaken when target is shifted two horizons(타깃을 두 지평선 밀면 우위가 약해져야 한다).",
            "required_metric": "balanced_accuracy and signal density collapse",
            "pass_condition": "control below actual and below 0.45",
            "forbidden_action": "do not tune threshold on this control(이 대조에서 임계값 조정 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "label_shift_gap48_control",
            "priority": "P0",
            "shift_or_block": "48 bars",
            "hypothesis": "slow state carry should fade after four horizons(네 지평선 뒤 느린 상태 이월이 약해져야 한다).",
            "required_metric": "balanced_accuracy and macro F1 collapse",
            "pass_condition": "control below actual and below 0.42",
            "forbidden_action": "do not choose model by this control(이 대조로 모델 선택 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "day_block_permutation_control",
            "priority": "P1",
            "shift_or_block": "daily blocks",
            "hypothesis": "calendar block carry may mimic edge(일 단위 상태 이월이 우위처럼 보일 수 있다).",
            "required_metric": "block permutation score near random",
            "pass_condition": "balanced_accuracy near 0.33",
            "forbidden_action": "do not use calendar block as filter(달력 블록을 필터로 사용 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "week_block_permutation_control",
            "priority": "P1",
            "shift_or_block": "weekly blocks",
            "hypothesis": "weekly regime carry may be overread(주 단위 레짐 이월을 과대해석할 수 있다).",
            "required_metric": "weekly block control collapse",
            "pass_condition": "control below actual",
            "forbidden_action": "do not fit to a known week pocket(알려진 주간 포켓 맞춤 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "purged_adjacent_split_control",
            "priority": "P0",
            "shift_or_block": "purged boundaries",
            "hypothesis": "adjacent split continuity inflates review score(인접 분할 연속성이 검토 점수를 부풀린다).",
            "required_metric": "validation/OOS gap and negative control clearance",
            "pass_condition": "all shifted controls clear before MT5 probe",
            "forbidden_action": "do not declare Forward Passed(전진 통과 선언 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_direction_flip_attribution(cl_negative: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cl_negative:
        if row["control_id"] != "direction_flip_control":
            continue
        rows.append(
            {
                "model_id": row["model_id"],
                "label_candidate_id": row["label_candidate_id"],
                "validation_control_balanced_accuracy": fnum(row["validation_control_balanced_accuracy"]),
                "oos_control_balanced_accuracy": fnum(row["oos_control_balanced_accuracy"]),
                "oos_actual_balanced_accuracy": fnum(row["oos_actual_balanced_accuracy"]),
                "interpretation": "single validation-side polarity warning(단일 검증 방향 극성 경고)",
                "repair_use": "review only; no polarity flip(검토 전용, 극성 반전 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_decision_matrix() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "cm_decision_hold_mt5_probe",
            "status": "held",
            "reason": "shifted_return_control(이동 수익률 대조)이 10개 모델을 막음",
            "next_action": NEXT_RUN_ID,
            "forbidden_action": "MT5 probe(탐침) 즉시 실행 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "cm_decision_open_cn_materialization",
            "status": "open_next",
            "reason": "purged/embargo split(제거/격리 분할)과 non-overlap controls(비중첩 대조)를 실제 입력으로 만들어야 함",
            "next_action": NEXT_RUN_ID,
            "forbidden_action": "새 후보 선택 또는 임계값 재조정 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "source model input timestamp order inherited; no new broker data used",
        "sample_scope": "train/validation/OOS labels through existing model input",
        "missing_or_duplicate_check": "input artifacts present; row-level duplicate check deferred to CN materialization",
        "feature_label_boundary": "CM diagnoses label serial memory and split adjacency before new training",
        "split_boundary": "design only; no fit or threshold selection",
        "leakage_risk": "serial dependence and adjacent split carry",
        "data_hash_or_identity": {"source_sha256": sha256_file(SOURCE_MODEL_INPUT)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no_model_training_design_only",
        "target_and_label": "label candidates from CK, reviewed for serial dependence",
        "split_method": "existing train/validation/OOS with proposed purged variants",
        "selection_metric": "not_applicable_no_selection",
        "secondary_metrics": "label autocorrelation, return autocorrelation, negative control plan",
        "threshold_policy": "not_touched",
        "overfit_risk": "selecting split/purge gap from CK model results",
        "calibration_risk": "not_applicable",
        "comparison_baseline": "CL negative-control review",
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in OUTPUT_FILES],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "label autocorrelation, return autocorrelation, purge contracts, negative-control plan",
        "evidence_missing": "CN materialized repair inputs and retraining outcome",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "부정 대조가 강한 이유를 라벨 연속성 문제로 보고, 다음에는 분할/대조 입력을 고친다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt["artifact_hashes"] = {rel(path): sha256_file(path) for path in paths if path != LINEAGE_RECEIPT and path_exists(path)}
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
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
        row("cm_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CL과 CK 입력을 모두 연결한다."),
        row("cm_gate_label_autocorr", final["label_autocorr_rows"] >= 150, final["label_autocorr_rows"], ">=150 rows", "라벨 연속성을 후보/분할/시차별로 본다."),
        row("cm_gate_return_autocorr", final["return_autocorr_rows"] >= 30, final["return_autocorr_rows"], ">=30 rows", "future return(미래 수익률) 기억을 본다."),
        row("cm_gate_purged_contracts", final["purged_contract_rows"] >= 4, final["purged_contract_rows"], ">=4 purge candidates", "제거/격리 분할 후보를 만든다."),
        row("cm_gate_nonoverlap_controls", final["nonoverlap_control_rows"] >= 5, final["nonoverlap_control_rows"], ">=5 controls", "비중첩 부정 대조를 사전 선언한다."),
        row("cm_gate_mt5_probe_still_held", final["mt5_runtime_probe"] == "held", final["mt5_runtime_probe"], "held", "수리 전 런타임 탐침을 열지 않는다."),
        row("cm_gate_no_training_or_selection", True, "training=not_run;selection=not_run", "no training/selection", "설계 결과를 새 승자로 바꾸지 않는다."),
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CM Serial Dependence Label Boundary Repair Design(연속 의존 라벨 경계 수리 설계)

## Conclusion(결론)

run337CM(337CM 실행)은 새 모델을 학습하지 않고, run337CL(337CL 실행)이 막은 shifted_return_control(이동 수익률 대조)을 수리 설계로 바꿨다.

Effect(효과): 다음 run337CN(337CN 실행)은 purged/embargo split(제거/격리 분할)과 non-overlap negative controls(비중첩 부정 대조)를 실제 학습 입력 후보로 물질화한다. MT5 runtime probe(MT5 런타임 탐침)는 계속 보류다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- label_autocorr_rows(라벨 자기상관 행): `{final["label_autocorr_rows"]}`
- return_autocorr_rows(수익률 자기상관 행): `{final["return_autocorr_rows"]}`
- max_lag12_label_balanced_accuracy(12봉 라벨 균형 정확도 최대): `{final["max_lag12_label_balanced_accuracy"]}`
- purged_contract_rows(제거 분할 계약 행): `{final["purged_contract_rows"]}`
- nonoverlap_control_rows(비중첩 대조 행): `{final["nonoverlap_control_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- new_training(새 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `held`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CM

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): serial dependence(연속 의존)와 split carry(분할 이월)를 수리하기 위한 CN materialization(물질화)을 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(LABEL_AUTOCORR)}`, `{rel(PURGED_SPLIT_CONTRACT)}`
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
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CM focus complete: serial-dependence label-boundary repair design(연속 의존 라벨 경계 수리 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CN(337CN 실행)에서 purged/embargo split(제거/격리 분할)과 non-overlap controls(비중첩 대조)를 물질화한다."
    )
    if "Stage337 run337CM focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CM focus complete:.*?(?=\n- >-\n  Stage337 run337CL|\n[A-Za-z0-9_]+:)",
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
## Stage337 run337CM(337CM 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): shifted_return_control(이동 수익률 대조)을 serial-dependence/purged split(연속 의존/제거 분할) 수리 설계로 바꿨다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CM\(337CM 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CL|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CL(337CL"
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
- actual_mt5_execution(실제 MT5 실행): `held_by_negative_control_repair_design`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 serial-dependence label-boundary repair input materialization(연속 의존 라벨 경계 수리 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CM(337CM 실행)" not in line)
    stage_entry = f"- {TODAY}: run337CM(337CM 실행) designed serial-dependence label-boundary repair(연속 의존 라벨 경계 수리). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CM designed serial-dependence label-boundary repair" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CM designed serial-dependence label-boundary repair(연속 의존 라벨 경계 수리) and opened `{NEXT_RUN_ID}`."
    changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "serial_dependence_label_boundary_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"label_autocorr_rows={final['label_autocorr_rows']};purge_contracts={final['purged_contract_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "serial_dependence_repair_design",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "diagnostic_design_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"max_lag12_label_balanced_accuracy={final['max_lag12_label_balanced_accuracy']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5_probe",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CL negative-control risk converted to repair design",
        "kpi_scope": "diagnostic_design_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "question": "how to repair shifted-return negative-control risk without overfitting",
        "metric_scope": "label_autocorr_return_autocorr_purge_design",
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
    df = read_source_frame()
    candidates = read_csv(LABEL_CANDIDATE_MATRIX)
    cl_negative = read_csv(CL_NEGATIVE_ATTRIBUTION)
    label_autocorr = build_label_autocorr(df, candidates)
    return_autocorr = build_return_autocorr(df)
    purged_contracts = build_purged_contracts()
    nonoverlap_controls = build_nonoverlap_controls()
    direction_flip = build_direction_flip_attribution(cl_negative)
    decision_matrix = build_decision_matrix()
    lag12_values = [
        fnum(row["balanced_accuracy_y_t_vs_y_t_minus_lag"])
        for row in label_autocorr
        if int(row["lag_bars"]) == 12
    ]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "source_rows": int(len(df)),
        "label_candidate_rows": len(candidates),
        "label_autocorr_rows": len(label_autocorr),
        "return_autocorr_rows": len(return_autocorr),
        "max_lag12_label_balanced_accuracy": max(lag12_values) if lag12_values else 0.0,
        "purged_contract_rows": len(purged_contracts),
        "nonoverlap_control_rows": len(nonoverlap_controls),
        "direction_flip_rows": len(direction_flip),
        "decision_rows": len(decision_matrix),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "held",
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
    artifacts: list[Path] = [
        write_csv(LABEL_AUTOCORR, LABEL_COLUMNS, label_autocorr),
        write_csv(RETURN_AUTOCORR, RETURN_COLUMNS, return_autocorr),
        write_csv(PURGED_SPLIT_CONTRACT, PURGE_COLUMNS, purged_contracts),
        write_csv(NONOVERLAP_CONTROL_PLAN, CONTROL_COLUMNS, nonoverlap_controls),
        write_csv(DIRECTION_FLIP_ATTRIBUTION, DIRECTION_COLUMNS, direction_flip),
        write_csv(REPAIR_DECISION_MATRIX, DECISION_COLUMNS, decision_matrix),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
