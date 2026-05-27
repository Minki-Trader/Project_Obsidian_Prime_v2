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
from stage_pipelines.stage337 import review_validation_support_control_residual_materialization as ds  # noqa: E402
from stage_pipelines.stage337 import materialize_validation_support_control_residual_repair_inputs as dr  # noqa: E402
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
STAGE_ID = ds.STAGE_ID
RUN_NUMBER = "run337DT"
RUN_ID = "run337DT_design_broad_validation_failure_control_residual_repair_without_db_v1"
PARENT_RUN_ID = ds.RUN_ID
NEXT_RUN_ID = "run337DU_materialize_broad_validation_failure_control_residual_repair_inputs_without_db_v1"
STATUS = "completed_stage337DT_broad_validation_failure_control_residual_repair_design_no_training_no_selection"
JUDGMENT = "broad_validation_failure_repair_design_ready_for_transfer_materialization"
DECISION = "stage337DT_open_run337DU_materialize_broad_validation_failure_control_residual_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DT_broad_validation_failure_control_residual_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ds.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ds.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DT_broad_validation_failure_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DT_broad_validation_failure_repair_design.md"
SELECTED_STATUS = ds.SELECTED_STATUS
STAGE_BRIEF = ds.STAGE_BRIEF
WORKSPACE_STATE = ds.WORKSPACE_STATE
CURRENT_STATE = ds.CURRENT_STATE
CHANGELOG = ds.CHANGELOG
RUN_REGISTRY = ds.RUN_REGISTRY
ALPHA_LEDGER = ds.ALPHA_LEDGER
ARTIFACT_REGISTRY = ds.ARTIFACT_REGISTRY
STAGE_LEDGER = ds.STAGE_LEDGER

DS_FINAL = ds.FINAL_DECISION
DS_GATES = ds.REQUIRED_GATE_AUDIT
DS_QUEUE = ds.DT_QUEUE
DS_TAPE_INTEGRITY = ds.TAPE_INTEGRITY_REVIEW
DS_VALIDATION_POCKET = ds.VALIDATION_POCKET_REVIEW
DS_CONTROL_RESIDUAL = ds.CONTROL_RESIDUAL_REVIEW
DS_QUARANTINE_FIREWALL = ds.QUARANTINE_FIREWALL_REVIEW
DR_PREDICTION_TAPE = dr.ALL_MODEL_PREDICTION_TAPE
DR_VALIDATION_SLICES = dr.VALIDATION_CURVE_POCKET_SLICES
DR_CONTROL_TAPE = dr.SHIFTED_CONTROL_RESIDUAL_TAPE
DR_QUARANTINE_LEDGER = dr.OOS_QUARANTINE_LEDGER

BROAD_VALIDATION_REPAIR_DESIGN = RUN_DIR / "broad_validation_failure_repair_design.csv"
SHIFTED_CONTROL_REPAIR_DESIGN = RUN_DIR / "shifted_control_residual_repair_design.csv"
FAMILY_SCOPE_CONSTRAINT_DESIGN = RUN_DIR / "family_scope_constraint_design.csv"
NO_RELEASE_FIREWALL_DESIGN = RUN_DIR / "no_release_firewall_design.csv"
DU_QUEUE = RUN_DIR / "run337DU_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DS_FINAL,
    DS_GATES,
    DS_QUEUE,
    DS_TAPE_INTEGRITY,
    DS_VALIDATION_POCKET,
    DS_CONTROL_RESIDUAL,
    DS_QUARANTINE_FIREWALL,
    DR_PREDICTION_TAPE,
    DR_VALIDATION_SLICES,
    DR_CONTROL_TAPE,
    DR_QUARANTINE_LEDGER,
)
OUTPUT_FILES = (
    BROAD_VALIDATION_REPAIR_DESIGN,
    SHIFTED_CONTROL_REPAIR_DESIGN,
    FAMILY_SCOPE_CONSTRAINT_DESIGN,
    NO_RELEASE_FIREWALL_DESIGN,
    DU_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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

BROAD_COLUMNS = (
    "design_id",
    "repair_lane",
    "observed_failure",
    "evidence_source",
    "repair_hypothesis",
    "materialization_plan",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "design_id",
    "control_subject",
    "affected_scope",
    "observed_blocker",
    "repair_hypothesis",
    "materialization_plan",
    "success_condition",
    "failure_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
FAMILY_COLUMNS = (
    "constraint_id",
    "scope_axis",
    "observed_status",
    "constraint_rule",
    "allowed_use",
    "forbidden_use",
    "next_materialization",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "allowed_next_action",
    "required_evidence_to_release",
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
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


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


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "pocket": pd.read_csv(io_path(DS_VALIDATION_POCKET)),
        "control": pd.read_csv(io_path(DS_CONTROL_RESIDUAL)),
        "quarantine": pd.read_csv(io_path(DS_QUARANTINE_FIREWALL)),
        "tape_integrity": pd.read_csv(io_path(DS_TAPE_INTEGRITY)),
    }


def broad_status_value(pocket: pd.DataFrame, family: str, column: str) -> Any:
    rows = pocket.loc[pocket["slice_family"].astype(str).eq(family)]
    if len(rows) == 0:
        return ""
    return rows.iloc[0].get(column, "")


def build_broad_design(frames: Mapping[str, pd.DataFrame], final: Mapping[str, Any]) -> list[dict[str, str]]:
    pocket = frames["pocket"]
    overall_ratio = as_float(final.get("overall_weak_slice_ratio"))
    worst_net = as_float(final.get("worst_net_log_return_after_cost"))
    worst_pf = as_float(final.get("worst_profit_factor"))
    return [
        {
            "design_id": "train_validation_transfer_matrix",
            "repair_lane": "defensive_diagnostic(방어 진단)",
            "observed_failure": f"overall weak slice ratio={overall_ratio}; worst_pf={worst_pf}",
            "evidence_source": rel(DS_VALIDATION_POCKET),
            "repair_hypothesis": "validation weakness is broad and must be compared against train-side behavior before new training(검증 약점이 넓어서 새 학습 전 학습 측 행동과 비교 필요)",
            "materialization_plan": "DU builds train/validation/OOS transfer matrix from existing model tape and source rows(DU가 기존 모델 테이프와 원천 행으로 학습/검증/OOS 전이 행렬 생성)",
            "success_condition": "train-to-validation failure mode is named without selecting models(모델 선택 없이 학습-검증 실패 양식 명명)",
            "failure_condition": "validation failure cannot be explained by transfer, density, control, or slice shape(전이/밀도/대조/슬라이스로 검증 실패 설명 불가)",
            "invalid_condition": "DU uses validation/OOS to tune thresholds or filter rows(DU가 검증/OOS로 임계값이나 행 필터 조정)",
            "forbidden_action": "no threshold tuning, no candidate selection(임계값 튜닝/후보 선택 금지)",
            "effect": "turns broad failure into transfer evidence(넓은 실패를 전이 근거로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "density_drawdown_pressure_matrix",
            "repair_lane": "repair_diagnostic(수리 진단)",
            "observed_failure": "validation is weak across cost/model/feature axes(비용/모델/피처 축 전반 검증 약함)",
            "evidence_source": rel(DS_VALIDATION_POCKET),
            "repair_hypothesis": "argmax action density is too broad and creates drawdown pressure(argmax 행동 밀도가 너무 넓어 드로다운 압력을 만듦)",
            "materialization_plan": "DU measures density, run-length, underwater stretch, and drawdown pockets per model/split(DU가 모델/분할별 밀도, 연속 구간, 침수 기간, 드로다운 포켓 측정)",
            "success_condition": "density/drawdown pressure is quantified before any new objective(새 목표 전 밀도/드로다운 압력 정량화)",
            "failure_condition": "density is not the driver and weakness remains broad(밀도가 원인이 아니고 약점이 넓게 유지)",
            "invalid_condition": "density result becomes a validation-tuned threshold(밀도 결과가 검증 튜닝 임계값으로 변함)",
            "forbidden_action": "no density threshold search(밀도 임계값 탐색 금지)",
            "effect": "separates action overbreadth from true signal weakness(행동 과다와 진짜 신호 약점 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "objective_rebuild_input_contract",
            "repair_lane": "aggressive_repair(공격 수리)",
            "observed_failure": f"worst validation net={worst_net}; all family axes broad or mixed weak(최악 검증 순손익 및 축 전반 약함)",
            "evidence_source": rel(DS_VALIDATION_POCKET),
            "repair_hypothesis": "a future ONNX may need a different train-only objective, not a selected threshold(미래 ONNX는 선택 임계값이 아니라 다른 학습 전용 목표가 필요할 수 있음)",
            "materialization_plan": "DU prepares train-only objective candidates for later review: abstention-aware cost target, drawdown-penalty tags, and direction residual tags(DU가 이후 검토용 학습 전용 목표 후보 입력 준비)",
            "success_condition": "objective inputs are materialized but not trained or selected(목표 입력만 물질화하고 학습/선택 없음)",
            "failure_condition": "objective rebuild inputs reuse validation/OOS outcomes as labels(목표 재구축 입력이 검증/OOS 결과를 라벨로 재사용)",
            "invalid_condition": "future training claims improvement before review(미래 학습이 검토 전 개선 주장)",
            "forbidden_action": "no new training in DT/DU(DT/DU 새 학습 금지)",
            "effect": "keeps aggressive repair available without overfit(공격 수리를 열어두되 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "macro_logreg_failure_memory",
            "repair_lane": "failure_memory(실패 기억)",
            "observed_failure": f"worst_slice={broad_status_value(pocket, 'all', 'worst_slice_value')}; worst_pf={worst_pf}",
            "evidence_source": rel(DS_VALIDATION_POCKET),
            "repair_hypothesis": "macro logistic family is a broad loss carrier, not a winner candidate(매크로 로지스틱 계열은 승자 후보가 아니라 넓은 손실 운반체)",
            "materialization_plan": "DU writes failure-memory rows for macro/logreg and all broad-axis failures(DU가 macro/logreg 및 넓은 축 실패 기억 행 기록)",
            "success_condition": "failure memory blocks accidental re-entry as selected family(실패 기억이 우발적 선택 재진입 차단)",
            "failure_condition": "same family is reintroduced as winner without new evidence(새 근거 없이 같은 계열이 승자로 재진입)",
            "invalid_condition": "failure memory is treated as permanent idea death(실패 기억을 영구 사망으로 취급)",
            "forbidden_action": "no winner pruning as selection(승자 가지치기를 선택으로 쓰기 금지)",
            "effect": "preserves lessons without killing exploration(교훈 보존, 탐색은 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "wfo_precheck_contract",
            "repair_lane": "defensive_forward_readiness(방어 전진 준비)",
            "observed_failure": "single split review is insufficient for operating claim(단일 분할 검토는 운영 주장에 부족)",
            "evidence_source": rel(DS_FINAL),
            "repair_hypothesis": "before another ONNX package, materialization must expose WFO readiness gaps(다음 ONNX 패키지 전 WFO 준비 공백 노출 필요)",
            "materialization_plan": "DU emits WFO precheck and embargo feasibility contract(DU가 WFO 사전검사와 embargo 가능성 계약 작성)",
            "success_condition": "future training packet has WFO/no-overfit prerequisites(미래 학습 묶음이 WFO/무과적합 전제 보유)",
            "failure_condition": "future packet proceeds with single split only(미래 묶음이 단일 분할만으로 진행)",
            "invalid_condition": "WFO is backfilled after model choice(WFO가 모델 선택 후 사후 보강)",
            "forbidden_action": "no Forward/Goal claim(전진/목표 주장 금지)",
            "effect": "keeps forward robustness standard alive(전진 강건성 기준 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_control_design(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, str]]:
    control = frames["control"]
    shifted_validation = control.loc[
        control["split"].astype(str).eq("validation")
        & control["control_id"].astype(str).eq("shifted_return_control")
    ]
    blocked_models = ""
    if len(shifted_validation):
        blocked_models = str(shifted_validation.iloc[0].get("blocked_models", ""))
    return [
        {
            "design_id": "technical_extratrees_shifted_residual_isolation",
            "control_subject": "shifted_return_control(이동 수익률 대조)",
            "affected_scope": blocked_models,
            "observed_blocker": "3 validation shifted-control blocks(검증 이동 대조 차단 3개)",
            "repair_hypothesis": "technical ExtraTrees may memorize serial action texture(technical ExtraTrees가 연속 행동 질감을 기억할 수 있음)",
            "materialization_plan": "DU isolates blocked models by hour/month/source-order run length(DU가 차단 모델을 시간/월/source 순서 연속 길이로 격리)",
            "success_condition": "shifted residual has localized signature or broad block is confirmed(이동 잔차 국소 서명 또는 넓은 차단 확인)",
            "failure_condition": "residual cannot be separated from candidate signal(잔차와 후보 신호 분리 실패)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "treats serial residual as a blocker, not noise(연속 잔차를 잡음이 아닌 차단으로 처리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fixed_control_policy_carry",
            "control_subject": "negative control policy(부정대조 정책)",
            "affected_scope": "all future repair packets(모든 미래 수리 묶음)",
            "observed_blocker": "control threshold already fixed in DP/DR/DS(DP/DR/DS에서 대조 기준 고정)",
            "repair_hypothesis": "control relaxation would create repair-overfit(대조 완화는 수리 과적합 생성)",
            "materialization_plan": "DU carries exact block rule alignment>=max(0.45,candidate-0.02)(DU가 동일 차단 규칙 전달)",
            "success_condition": "control policy unchanged in DU output(DU 출력에서 대조 정책 불변)",
            "failure_condition": "control policy changes to pass a branch(분기 통과를 위해 대조 정책 변경)",
            "forbidden_action": "no control retuning(대조 재튜닝 금지)",
            "effect": "keeps overfit guard stable(과적합 방어 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "non_blocking_control_floor_carry",
            "control_subject": "noise and block-shuffle controls(잡음 및 블록 셔플 대조)",
            "affected_scope": "validation and OOS(검증 및 OOS)",
            "observed_blocker": "noise/block shuffle are clear but remain required(잡음/블록 셔플은 통과했지만 계속 필요)",
            "repair_hypothesis": "passing controls define minimum audit breadth(통과 대조도 최소 감사 폭을 정의)",
            "materialization_plan": "DU carries non-blocking controls into repair input contract(DU가 비차단 대조를 수리 입력 계약에 전달)",
            "success_condition": "future materialization keeps all controls(미래 물질화가 모든 대조 유지)",
            "failure_condition": "passing controls are dropped(통과 대조 삭제)",
            "forbidden_action": "no control deletion(대조 삭제 금지)",
            "effect": "keeps audit breadth intact(감사 폭 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_family_constraints(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, str]]:
    pocket = frames["pocket"]
    rows: list[dict[str, str]] = []
    for axis in ("cost_policy", "feature_set", "model_config", "month", "hour", "all"):
        axis_rows = pocket.loc[pocket["slice_family"].astype(str).eq(axis)]
        if len(axis_rows) == 0:
            continue
        row = axis_rows.iloc[0]
        weak_ratio = as_float(row.get("weak_slice_ratio"))
        status = str(row.get("review_status", ""))
        if weak_ratio >= 0.75:
            constraint = "do_not_select_axis_or_filter; materialize transfer/failure constraints only(축/필터 선택 금지, 전이/실패 제약만 물질화)"
        elif weak_ratio >= 0.35:
            constraint = "mixed_axis_requires_stability_check_before_any_repair(혼합 축은 수리 전 안정성 검사 필요)"
        else:
            constraint = "localized_axis_diagnostic_only(국소 축 진단 전용)"
        rows.append(
            {
                "constraint_id": f"family_scope__{axis}",
                "scope_axis": axis,
                "observed_status": f"{status};weak_ratio={weak_ratio}",
                "constraint_rule": constraint,
                "allowed_use": "failure memory, transfer matrix, repair design(실패 기억/전이 행렬/수리 설계)",
                "forbidden_use": "winner selection, release filter, MT5 queue(승자 선택/해제 필터/MT5 대기열)",
                "next_materialization": NEXT_RUN_ID,
                "effect": "keeps weak axes as constraints rather than winners(약한 축을 승자가 아닌 제약으로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "constraint_id": "quarantine_oos_only_lift",
            "scope_axis": "oos_quarantine",
            "observed_status": "10 OOS-only lift rows quarantined(OOS 단독 개선 10행 격리)",
            "constraint_rule": "quarantine rows may inform failure memory only(격리 행은 실패 기억에만 사용)",
            "allowed_use": "attribution and negative memory(귀인과 부정 기억)",
            "forbidden_use": "shortlist or candidate selection(후보 목록 또는 후보 선택)",
            "next_materialization": NEXT_RUN_ID,
            "effect": "prevents attractive OOS pockets from driving overfit(매력적 OOS 포켓 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_firewall_design() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_candidate_selection",
            "blocked_action_or_claim": "candidate selection(후보 선택)",
            "blocked_reason": "broad validation failure ratio above 0.75(넓은 검증 실패 비율 0.75 초과)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "future reviewed repair with validation/control gates passed(미래 검토된 수리의 검증/대조 게이트 통과)",
            "effect": "keeps design from becoming promotion(설계가 승격으로 변하는 것 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_threshold_tuning",
            "blocked_action_or_claim": "threshold tuning(임계값 튜닝)",
            "blocked_reason": "row tape exposes many weak slices and would invite slice mining(행 테이프가 많은 약한 슬라이스를 보여 필터 채굴 유혹)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "train-only threshold policy in a separate reviewed packet(별도 검토 묶음의 학습 전용 임계값 정책)",
            "effect": "prevents validation-overfit repair(검증 과적합 수리 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_probe",
            "blocked_action_or_claim": "MT5 runtime probe(MT5 런타임 탐침)",
            "blocked_reason": "validation and shifted-control blockers unresolved(검증과 이동 대조 차단 미해결)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "repaired materialization/training review before runtime(런타임 전 수리 물질화/학습 검토)",
            "effect": "keeps runtime claims closed(런타임 주장 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_forward_or_goal",
            "blocked_action_or_claim": "Forward Passed/Failed and Goal Achieve(전진 통과/실패 및 목표 달성)",
            "blocked_reason": "DT is design-only and uses no new forward/MT5 evidence(DT는 설계 전용이며 새 전진/MT5 근거 없음)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "actual forward/runtime evidence with gates(게이트가 있는 실제 전진/런타임 근거)",
            "effect": "prevents premature completion claim(조기 완료 주장 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_du_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DU_materialize_train_validation_transfer_matrix",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-validation-OOS transfer matrix(학습-검증-OOS 전이 행렬 물질화)",
            "required_inputs": f"{rel(BROAD_VALIDATION_REPAIR_DESIGN)};{rel(DR_PREDICTION_TAPE)}",
            "required_outputs": "train_validation_transfer_matrix.csv",
            "blocked_if_missing": "broad repair design or prediction tape(넓은 수리 설계 또는 예측 테이프)",
            "forbidden_action": "no winner selection(승자 선택 금지)",
            "effect": "checks if failure is transfer/regime driven(실패가 전이/레짐 원인인지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DU_materialize_density_drawdown_pressure",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize density/drawdown pressure inputs(밀도/드로다운 압력 입력 물질화)",
            "required_inputs": f"{rel(BROAD_VALIDATION_REPAIR_DESIGN)};{rel(DR_VALIDATION_SLICES)}",
            "required_outputs": "density_drawdown_pressure_matrix.csv",
            "blocked_if_missing": "validation slices(검증 슬라이스)",
            "forbidden_action": "no density threshold search(밀도 임계값 탐색 금지)",
            "effect": "tests whether action overbreadth drives drawdown(행동 과다가 드로다운을 만드는지 검사)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DU_materialize_control_residual_isolation",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize shifted-control residual isolation matrix(이동 대조 잔차 격리 행렬 물질화)",
            "required_inputs": f"{rel(SHIFTED_CONTROL_REPAIR_DESIGN)};{rel(DR_CONTROL_TAPE)}",
            "required_outputs": "shifted_control_residual_isolation_matrix.csv",
            "blocked_if_missing": "control residual design or tape(대조 잔차 설계 또는 테이프)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "isolates serial dependence risk(연속 의존 위험 격리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DU_materialize_family_scope_constraints",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize family scope constraints and failure memory(계열 범위 제약과 실패 기억 물질화)",
            "required_inputs": rel(FAMILY_SCOPE_CONSTRAINT_DESIGN),
            "required_outputs": "family_scope_constraint_matrix.csv;failure_memory_update.csv",
            "blocked_if_missing": "family scope constraints(계열 범위 제약)",
            "forbidden_action": "no family winner pruning(계열 승자 가지치기 금지)",
            "effect": "keeps weak axes as constraints(약한 축을 제약으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DU_materialize_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize no-release firewall carry(무해제 방화벽 전달 물질화)",
            "required_inputs": rel(NO_RELEASE_FIREWALL_DESIGN),
            "required_outputs": "no_release_firewall_carry.csv",
            "blocked_if_missing": "no-release firewall design(무해제 방화벽 설계)",
            "forbidden_action": "no MT5/Forward/Goal claim(MT5/전진/목표 주장 금지)",
            "effect": "preserves operating boundary(운영 경계 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DS/DR inputs exist(필수 DS/DR 입력 존재)"),
        ("parent_ds_gates_passed", final["ds_failed_gate_rows"] == 0, str(final["ds_failed_gate_rows"]), "0", "DS review usable(DS 검토 사용 가능)"),
        ("parent_next_action_matches", final["ds_next_action"] == RUN_ID, str(final["ds_next_action"]), RUN_ID, "continues DS queue(DS 대기열을 이어감)"),
        ("broad_failure_evidence_present", final["overall_weak_slice_ratio"] >= 0.75, str(final["overall_weak_slice_ratio"]), ">=0.75", "broad failure evidence present(넓은 실패 근거 존재)"),
        ("broad_design_materialized", final["broad_design_rows"] >= 5, str(final["broad_design_rows"]), ">=5", "broad repair design exists(넓은 수리 설계 존재)"),
        ("control_design_materialized", final["control_design_rows"] >= 3, str(final["control_design_rows"]), ">=3", "control repair design exists(대조 수리 설계 존재)"),
        ("family_constraints_materialized", final["family_constraint_rows"] >= 6, str(final["family_constraint_rows"]), ">=6", "family constraints exist(계열 제약 존재)"),
        ("firewall_materialized", final["firewall_rows"] >= 4, str(final["firewall_rows"]), ">=4", "no-release firewall exists(무해제 방화벽 존재)"),
        ("du_queue_materialized", final["du_queue_rows"] == 5, str(final["du_queue_rows"]), "5", "DU materialization queue opened(DU 물질화 대기열 열림)"),
        (
            "no_forbidden_claim",
            final["model_training"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
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
    experiment_receipt = {
        "hypothesis": "broad validation failure requires transfer/density/control repair inputs before any new training(넓은 검증 실패는 새 학습 전 전이/밀도/대조 수리 입력 필요)",
        "comparison_baseline": rel(DS_FINAL),
        "controls": "no threshold tuning, no selection, fixed negative control policy(임계값 튜닝 없음/선택 없음/고정 부정대조 정책)",
        "stop_conditions": "any selection, MT5, Forward, or Goal claim(선택/MT5/전진/목표 주장 발생)",
        "success_criteria": "DU materializes transfer, density, control, family, firewall inputs(DU가 전이/밀도/대조/계열/방화벽 입력 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DS/DR source_row_id UTC row tape(DS/DR source_row_id UTC 행 테이프 상속)",
        "sample_scope": f"weak_slice_ratio={final['overall_weak_slice_ratio']};control_blocks={final['control_block_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "design-only; no feature/label recomputation(설계 전용, 피처/라벨 재계산 없음)",
        "split_boundary": "validation/OOS review drives design; train transfer only for future DU(검증/OOS 검토가 설계 입력, 학습 전이는 DU 예정)",
        "leakage_risk": "turning validation slices into tuned filters(검증 슬라이스를 튜닝 필터로 바꾸는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_design_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "design from DR/DS row-level review(DR/DS 행 단위 검토 기반 설계)",
        "target_and_label": "unchanged DO costed action label for evidence only(DO 비용 반영 행동 라벨 근거 전용 유지)",
        "split_method": "review-only, no training(검토 전용, 학습 없음)",
        "selection_metric": "none; broad failure blocks selection(없음, 넓은 실패가 선택 차단)",
        "secondary_metrics": "weak slice ratio, shifted control blocks, density/drawdown planned(약한 슬라이스 비율/이동 대조 차단/밀도 드로다운 예정)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "using broad-failure analysis as slice filters(넓은 실패 분석을 슬라이스 필터로 쓰는 위험)",
        "calibration_risk": "scores remain diagnostics(점수는 진단 전용)",
        "comparison_baseline": rel(DS_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"overall_weak_slice_ratio={final['overall_weak_slice_ratio']};control_block_rows={final['control_block_rows']}",
        "comparison_baseline": rel(DS_FINAL),
        "likely_drivers": "broad axis failure, action density, serial residual(넓은 축 실패/행동 밀도/연속 잔차)",
        "segment_checks": "designed for DU materialization(DU 물질화로 설계됨)",
        "trade_shape": "DS showed worst_pf and weak slice breadth(DS가 최악 PF와 약한 슬라이스 폭 제시)",
        "alternative_explanations": "proxy cost mismatch, regime transfer, target/action mismatch(프록시 비용 불일치/레짐 전이/목표 행동 불일치)",
        "attribution_confidence": "medium_for_design_low_for_runtime(설계는 중간, 런타임은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DT design contracts and DS review evidence(DT 설계 계약과 DS 검토 근거)",
        "evidence_missing": "DU materialization, later training/review, MT5, forward evidence(DU 물질화/이후 학습 검토/MT5/전진 근거)",
        "judgment_label": "design_completed_materialization_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "넓은 검증 실패라서 지금은 고르는 게 아니라 전이/밀도/대조 원인을 더 파야 한다.",
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_design_outputs_with_tracked_report(무시된 설계 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DT Broad Validation Failure Repair Design(넓은 검증 실패 수리 설계)

## Conclusion(결론)

run337DT(337DT 실행)는 run337DS(337DS 실행)의 broad validation failure(넓은 검증 실패)와 shifted-control residual(이동 대조 잔차)을 다음 DU materialization(물질화) 계약으로 바꿨다.

이 작업은 design-only(설계 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DU(337DU 실행)는 train-validation transfer(학습-검증 전이), density/drawdown pressure(밀도/드로다운 압력), control residual isolation(대조 잔차 격리), family constraints(계열 제약), no-release firewall(무해제 방화벽)을 물질화한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- overall_weak_slice_ratio(전체 약한 슬라이스 비율): `{final["overall_weak_slice_ratio"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- broad_design_rows(넓은 설계 행): `{final["broad_design_rows"]}`
- control_design_rows(대조 설계 행): `{final["control_design_rows"]}`
- family_constraint_rows(계열 제약 행): `{final["family_constraint_rows"]}`
- du_queue_rows(DU 대기열 행): `{final["du_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DT

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 넓은 검증 실패와 이동 대조 잔차를 DU 물질화 계약으로 넘기고 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(BROAD_VALIDATION_REPAIR_DESIGN)}`, `{rel(SHIFTED_CONTROL_REPAIR_DESIGN)}`
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
        f"  Stage337 run337DT focus complete: broad validation failure/control residual repair design(넓은 검증 실패/대조 잔차 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DU(337DU 실행)에서 train-validation transfer/density/control repair inputs(학습-검증 전이/밀도/대조 수리 입력)을 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DT focus complete")
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
    section = f"""## Stage337 run337DT(337DT 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 넓은 검증 실패와 이동 대조 잔차를 수리 입력 물질화로 넘겼지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DT(337DT 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dt_design_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 train-validation transfer/density/control repair input materialization(학습-검증 전이/밀도/대조 수리 입력 물질화)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DT(337DT 실행) designed broad validation failure/control residual repair and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DT(337DT 실행) designed broad validation failure"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DT designed broad validation failure/control residual repair and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DT designed broad validation failure"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broad_validation_failure_control_residual_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"weak_slice_ratio={final['overall_weak_slice_ratio']};control_blocks={final['control_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_from_row_level_review",
        "scoreboard_lane": "experiment_design_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"broad_design_rows={final['broad_design_rows']};du_queue_rows={final['du_queue_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "broad validation/control repair design materialized",
        "kpi_scope": "weak_slice_ratio_control_blocks_design_rows",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "question": "how to repair broad validation failure without selecting winners",
        "metric_scope": "design_rows_queue_rows",
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
    frames = load_frames()
    ds_final = read_json(DS_FINAL)
    ds_failed_gate_rows = sum(1 for row in read_csv(DS_GATES) if row.get("status") != "passed")
    broad_rows = build_broad_design(frames, ds_final)
    control_rows = build_control_design(frames)
    family_rows = build_family_constraints(frames)
    firewall_rows = build_firewall_design()
    queue_rows = build_du_queue()
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ds_next_action": ds_final.get("next_action", ""),
        "ds_failed_gate_rows": ds_failed_gate_rows,
        "missing_inputs": len(missing),
        "overall_weak_slice_ratio": as_float(ds_final.get("overall_weak_slice_ratio")),
        "control_block_rows": as_int(ds_final.get("control_block_rows")),
        "broad_design_rows": len(broad_rows),
        "control_design_rows": len(control_rows),
        "family_constraint_rows": len(family_rows),
        "firewall_rows": len(firewall_rows),
        "du_queue_rows": len(queue_rows),
        "model_training": "not_run",
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
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts: list[Path] = [
        write_csv(BROAD_VALIDATION_REPAIR_DESIGN, BROAD_COLUMNS, broad_rows),
        write_csv(SHIFTED_CONTROL_REPAIR_DESIGN, CONTROL_COLUMNS, control_rows),
        write_csv(FAMILY_SCOPE_CONSTRAINT_DESIGN, FAMILY_COLUMNS, family_rows),
        write_csv(NO_RELEASE_FIREWALL_DESIGN, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DU_QUEUE, QUEUE_COLUMNS, queue_rows),
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
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
