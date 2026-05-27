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
RUN_NUMBER = "run337CQ"
RUN_ID = "run337CQ_design_weak_density_and_control_alignment_repair_without_db_v1"
PARENT_RUN_ID = "run337CP_review_purged_serial_dependence_guarded_training_controls_without_db_v1"
NEXT_RUN_ID = "run337CR_materialize_weak_density_control_alignment_repair_inputs_without_db_v1"
STATUS = "completed_stage337CQ_weak_density_control_alignment_repair_design_no_training_no_selection"
JUDGMENT = "repair_design_required_for_calendar_carry_shift_residual_and_weak_density_before_any_mt5_probe"
DECISION = "stage337CQ_open_run337CR_materialize_weak_density_control_alignment_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CQ_weak_density_control_alignment_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CQ_weak_density_control_alignment_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CQ_weak_density_control_alignment_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CP_DIR = STAGE_DIR / "02_runs" / "run337CP"
CP_FINAL = CP_DIR / "final_decision.json"
CP_GATES = CP_DIR / "required_gate_coverage_audit.csv"
CP_MODEL_REVIEW = CP_DIR / "model_control_review_matrix.csv"
CP_BLOCKED_ATTRIBUTION = CP_DIR / "blocked_control_attribution.csv"
CP_WEAKNESS = CP_DIR / "review_ready_weakness_matrix.csv"
CP_MT5_REVIEW = CP_DIR / "mt5_probe_disposition_review.csv"
CP_QUEUE = CP_DIR / "run337CQ_repair_design_queue.csv"

DAY_BLOCK_DESIGN = RUN_DIR / "day_block_alignment_repair_design.csv"
SHIFT_RESIDUAL_DESIGN = RUN_DIR / "shift_residual_repair_design.csv"
WEAK_DENSITY_DESIGN = RUN_DIR / "weak_density_repair_design.csv"
BALANCE_MATRIX = RUN_DIR / "attack_defense_repair_balance_matrix.csv"
NO_MT5_RELEASE_NOTE = RUN_DIR / "no_mt5_probe_release_until_repair_review.md"
CR_QUEUE = RUN_DIR / "run337CR_materialization_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CP_FINAL,
    CP_GATES,
    CP_MODEL_REVIEW,
    CP_BLOCKED_ATTRIBUTION,
    CP_WEAKNESS,
    CP_MT5_REVIEW,
    CP_QUEUE,
)
OUTPUT_FILES = (
    DAY_BLOCK_DESIGN,
    SHIFT_RESIDUAL_DESIGN,
    WEAK_DENSITY_DESIGN,
    BALANCE_MATRIX,
    NO_MT5_RELEASE_NOTE,
    CR_QUEUE,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    PERFORMANCE_RECEIPT,
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

DAY_BLOCK_COLUMNS = (
    "design_id",
    "observed_issue",
    "hypothesis",
    "materialize_inputs",
    "required_slices",
    "pass_condition",
    "failure_condition",
    "forbidden_action",
    "next_run_id",
    "claim_boundary",
)
SHIFT_COLUMNS = (
    "design_id",
    "observed_issue",
    "hypothesis",
    "materialize_inputs",
    "required_controls",
    "pass_condition",
    "failure_condition",
    "forbidden_action",
    "next_run_id",
    "claim_boundary",
)
WEAK_COLUMNS = (
    "design_id",
    "observed_issue",
    "hypothesis",
    "materialize_inputs",
    "train_only_policy",
    "validation_gate",
    "oos_gate",
    "forbidden_action",
    "next_run_id",
    "claim_boundary",
)
BALANCE_COLUMNS = (
    "lane_id",
    "lane_type",
    "purpose",
    "required_input",
    "required_output",
    "blocks_if",
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


def numeric(value: Any, default: float = 0.0) -> float:
    if value is None or value == "" or pd.isna(value):
        return default
    return float(value)


def mean_column(rows: Sequence[Mapping[str, str]], column: str) -> float:
    values = [numeric(row.get(column, "")) for row in rows]
    return float(sum(values) / len(values)) if values else 0.0


def blocked_count(blocked_rows: Sequence[Mapping[str, str]], control_id: str) -> int:
    return sum(1 for row in blocked_rows if row.get("control_id") == control_id)


def blocked_models_for_control(blocked_rows: Sequence[Mapping[str, str]], control_id: str) -> int:
    for row in blocked_rows:
        if row.get("control_id") == control_id:
            return int(float(row.get("blocked_models", 0) or 0))
    return 0


def build_day_block_design(blocked_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    day_rows = [row for row in blocked_rows if row.get("control_id") == "day_block_permutation_control"]
    observed = f"day_block_blocks={day_rows[0].get('blocked_rows', '0') if day_rows else 0};avg_oos_control={mean_column(day_rows, 'avg_oos_control_balanced_accuracy'):.4f}"
    return [
        {
            "design_id": "day_block_session_calendar_attribution",
            "observed_issue": observed,
            "hypothesis": "day block permutation(일 단위 블록 순열)이 실제와 비슷하면 signal(신호)이 하루 단위 regime carry(레짐 이월)를 외우는 위험이 있다.",
            "materialize_inputs": "hour/session/day_of_week/month volatility slices(시간/세션/요일/월 변동성 조각) and per-day prediction concentration(일별 예측 집중도)",
            "required_slices": "US cash session(미국 정규장);pre/post cash(장전/장후);hour bucket(시간 버킷);weekday(요일);month(월);volatility tercile(변동성 3분위)",
            "pass_condition": "day block control(일 블록 대조)이 actual signal(실제 신호)보다 낮고, 성과가 특정 날짜 포켓에 집중되지 않음",
            "failure_condition": "one or two date pockets explain most edge(한두 날짜 포켓이 대부분 엣지 설명) or day control stays close to actual(일 대조가 실제에 가까움)",
            "forbidden_action": "do not drop profitable days or tune calendar filters from OOS(OOS 수익일 제거/달력 필터 튜닝 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "day_block_train_only_leave_day_family",
            "observed_issue": observed,
            "hypothesis": "train-only leave-day family(학습 전용 일 제거 계열)로도 신호가 유지되어야 calendar memorization(달력 암기) 위험이 줄어든다.",
            "materialize_inputs": "train-only leave-one-day-family masks(학습 전용 일 계열 제거 마스크) and validation/OOS read-only evaluation plan(검증/OOS 읽기 전용 평가 계획)",
            "required_slices": "train day family only(학습 구간 날짜 계열만);validation/OOS no-fit read(검증/OOS 적합 금지 판독)",
            "pass_condition": "train-only masks(학습 전용 마스크)에서 control clearance(대조 통과) and signal density(신호 밀도) 유지",
            "failure_condition": "mask family success depends on validation/OOS choice(검증/OOS 선택에 의존)",
            "forbidden_action": "do not choose mask by OOS PnL(OOS 손익으로 마스크 선택 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_shift_design(blocked_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    gap24 = [row for row in blocked_rows if row.get("control_id") == "label_shift_gap24_control"]
    gap48 = [row for row in blocked_rows if row.get("control_id") == "label_shift_gap48_control"]
    observed = (
        f"gap24_blocks={gap24[0].get('blocked_rows', '0') if gap24 else 0};"
        f"gap48_blocks={gap48[0].get('blocked_rows', '0') if gap48 else 0}"
    )
    return [
        {
            "design_id": "nonoverlap_horizon_family_extension",
            "observed_issue": observed,
            "hypothesis": "gap24/gap48 shift residual(이동 잔차)이 남으면 12-bar horizon(12봉 기간) 주변 상태 이월이 아직 모델 점수를 부풀릴 수 있다.",
            "materialize_inputs": "gap72/gap96 shift controls(72/96봉 이동 대조), horizon-disjoint row masks(기간 비중첩 행 마스크), source_row_id parity checks(원천 행 ID 동등성 확인)",
            "required_controls": "label_shift_gap72_control(72봉 이동 대조);label_shift_gap96_control(96봉 이동 대조);horizon_modulo_fold_control(기간 모듈로 폴드 대조)",
            "pass_condition": "all shifted controls(모든 이동 대조)가 actual(실제)보다 낮고 predeclared limit(사전 선언 한계) 미만",
            "failure_condition": "any shift control(이동 대조)이 actual(실제)과 비슷하거나 더 강함",
            "forbidden_action": "do not select purge gap or horizon by profit(수익으로 제거 간격/기간 선택 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "feature_state_carry_firewall",
            "observed_issue": observed,
            "hypothesis": "slow features(느린 피처) and stale context(낡은 문맥)가 label shift(라벨 이동)에도 맞아 보이는 state carry(상태 이월)를 만들 수 있다.",
            "materialize_inputs": "feature autocorrelation buckets(피처 자기상관 버킷), stale source age flags(낡은 원천 나이 플래그), technical-only vs macro/equity branches(기술 전용 대 거시/주식 분기)",
            "required_controls": "stale_context_carry_control(낡은 문맥 이월 대조);technical_only_control(기술 전용 대조);macro_equity_lag_control(거시/주식 지연 대조)",
            "pass_condition": "edge(엣지)가 stale context(낡은 문맥) 제거 후에도 유지되고 shift controls(이동 대조)가 약해짐",
            "failure_condition": "edge disappears when stale/context features are removed(낡은/문맥 피처 제거 시 엣지 소멸)",
            "forbidden_action": "do not keep stale feature because it improves OOS(OOS 개선 때문에 낡은 피처 유지 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_weak_density_design(weak_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    avg_validation = mean_column(weak_rows, "validation_balanced_accuracy")
    avg_oos = mean_column(weak_rows, "oos_balanced_accuracy")
    avg_density = mean_column(weak_rows, "oos_signal_density")
    observed = f"weak_models={len(weak_rows)};avg_validation_bal={avg_validation:.4f};avg_oos_bal={avg_oos:.4f};avg_oos_density={avg_density:.4f}"
    return [
        {
            "design_id": "train_only_density_budget_attack",
            "observed_issue": observed,
            "hypothesis": "control-passed volnorm(대조 통과 변동성 정규화) 신호는 너무 희소하므로 train-only density budget(학습 전용 밀도 예산)을 사전 선언해야 거래수를 늘릴 수 있다.",
            "materialize_inputs": "train-only score quantile bands(학습 전용 점수 분위 밴드), minimum density floors(최소 밀도 하한), no OOS tuning locks(OOS 튜닝 잠금)",
            "train_only_policy": "density floor candidates(밀도 하한 후보)는 train split(학습 분할)에서만 산출하고 validation/OOS(검증/OOS)는 읽기 전용",
            "validation_gate": "validation balanced_accuracy(검증 균형 정확도) >= 0.40 and signal_density(신호 밀도) >= 0.03",
            "oos_gate": "OOS balanced_accuracy(OOS 균형 정확도) >= 0.40 and controls(대조) below actual(실제)",
            "forbidden_action": "do not lower thresholds after seeing OOS trades(OOS 거래를 보고 임계값 낮추기 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "cost_curve_shape_attack_without_oos_selection",
            "observed_issue": observed,
            "hypothesis": "explosive return(폭발 수익률)을 향하려면 weak classifier(약한 분류기)보다 trade shape(거래 모양), cost ladder(비용 사다리), curve pocket(곡선 포켓)을 train-only 설계로 같이 보아야 한다.",
            "materialize_inputs": "predeclared cost ladder(사전 선언 비용 사다리), trade density bins(거래 밀도 구간), curve pocket stress plan(곡선 포켓 압박 계획)",
            "train_only_policy": "attack lanes(공격 레인)은 train-only floor(학습 전용 하한)로 만들고 validation/OOS에서 폐기 여부만 판정",
            "validation_gate": "no single session/date pocket(단일 세션/날짜 포켓 없음) and cost+1/+2 survival(비용 +1/+2 생존)",
            "oos_gate": "no curve pocket break(곡선 포켓 붕괴 없음), no control block(대조 차단 없음)",
            "forbidden_action": "do not optimize lot or threshold(로트/임계값 최적화 금지)",
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_balance_matrix() -> list[dict[str, str]]:
    return [
        {
            "lane_id": "defense_day_block_and_shift_controls",
            "lane_type": "defense(방어)",
            "purpose": "calendar carry(달력 이월) and serial dependence(연속 의존) 위험을 먼저 차단",
            "required_input": rel(CP_BLOCKED_ATTRIBUTION),
            "required_output": rel(DAY_BLOCK_DESIGN) + ";" + rel(SHIFT_RESIDUAL_DESIGN),
            "blocks_if": "day/shift controls(일/이동 대조)가 actual signal(실제 신호)과 분리되지 않음",
            "effect": "overfit repair(과적합 수리)를 성과 추구보다 앞에 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "attack_density_cost_curve_shape",
            "lane_type": "attack(공격)",
            "purpose": "trade count(거래수), cost survival(비용 생존), curve shape(곡선 모양)을 train-only(학습 전용)로 공격",
            "required_input": rel(CP_WEAKNESS),
            "required_output": rel(WEAK_DENSITY_DESIGN),
            "blocks_if": "density(밀도)를 OOS(실외표본)로 조정하거나 controls(대조)를 통과하지 못함",
            "effect": "사용 가능한 ONNX(온엑스)를 향한 공격성을 유지하되 OOS 맞춤을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "repair_materialization_firewall",
            "lane_type": "repair(수리)",
            "purpose": "CR에서 입력만 만들고 CS에서 제한 학습, CT에서 리뷰하는 순서를 고정",
            "required_input": rel(CR_QUEUE),
            "required_output": "run337CR materialized controls and train-only density inputs(CR 대조와 학습 전용 밀도 입력)",
            "blocks_if": "missing lineage/hash/gates(계보/해시/게이트 누락)",
            "effect": "수리 설계가 즉시 운영 주장으로 튀지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "runtime_probe_lock",
            "lane_type": "runtime-parity(런타임 동등성)",
            "purpose": "MT5 probe(MT5 탐침)는 control/signal/cost gates(대조/신호/비용 게이트) 이후에만 해제",
            "required_input": rel(NO_MT5_RELEASE_NOTE),
            "required_output": "mt5_probe_release_policy(탐침 해제 정책)",
            "blocks_if": "any model remains weak/control-blocked(모델이 약하거나 대조 차단)",
            "effect": "proxy(프록시) 성과를 runtime authority(런타임 권위)로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cr_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CR_materialize_day_block_and_session_slices",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "day/session/regime slices(일/세션/레짐 조각)와 per-day prediction concentration(일별 예측 집중도) 입력 물질화",
            "required_inputs": rel(DAY_BLOCK_DESIGN) + ";" + rel(CP_MODEL_REVIEW),
            "required_outputs": "day_session_regime_slice_frame.parquet;day_block_concentration_matrix.csv",
            "blocked_if_missing": "CO/CP model review(모델 검토) or source timestamps(원천 시각) missing",
            "forbidden_action": "do not drop days or tune filters from OOS(OOS로 날짜 제거/필터 튜닝 금지)",
            "effect": "calendar carry(달력 이월) 위험을 행 단위 입력으로 분해한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CR_materialize_shift_and_state_carry_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "gap72/gap96/horizon modulo/stale feature controls(72/96봉/기간 모듈로/낡은 피처 대조) 입력 물질화",
            "required_inputs": rel(SHIFT_RESIDUAL_DESIGN) + ";" + rel(CP_BLOCKED_ATTRIBUTION),
            "required_outputs": "extended_shift_control_frame.parquet;feature_state_carry_matrix.csv",
            "blocked_if_missing": "source row id parity(원천 행 ID 동등성) missing",
            "forbidden_action": "do not choose control by profit(수익으로 대조 선택 금지)",
            "effect": "serial dependence(연속 의존)와 stale context(낡은 문맥) 위험을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CR_materialize_train_only_density_attack_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "train-only density/cost/curve attack inputs(학습 전용 밀도/비용/곡선 공격 입력) 물질화",
            "required_inputs": rel(WEAK_DENSITY_DESIGN) + ";" + rel(CP_WEAKNESS),
            "required_outputs": "train_only_density_policy_grid.csv;cost_curve_shape_gate_contract.csv",
            "blocked_if_missing": "train split only policy(학습 분할 전용 정책) missing",
            "forbidden_action": "do not lower threshold from validation/OOS(검증/OOS로 임계값 낮추기 금지)",
            "effect": "거래수와 곡선 품질을 공격하지만 과최적화 경로를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CR_materialize_mt5_probe_release_lock",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "MT5 probe release lock(MT5 탐침 해제 잠금)과 proxy-to-MT5 comparison requirement(프록시-MT5 비교 요구) 물질화",
            "required_inputs": rel(NO_MT5_RELEASE_NOTE),
            "required_outputs": "mt5_probe_release_lock.csv;proxy_mt5_required_compare_contract.csv",
            "blocked_if_missing": "control/signal/cost gates(대조/신호/비용 게이트) missing",
            "forbidden_action": "do not run MT5 probe from weak/control-blocked model(약하거나 대조 차단 모델 MT5 실행 금지)",
            "effect": "proxy result(프록시 결과)와 MT5 runtime probe(MT5 런타임 탐침) 차이를 반드시 비교하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_no_mt5_note(final: Mapping[str, Any]) -> Path:
    text = f"""# No MT5 Probe Release Until Repair Review(MT5 탐침 해제 보류)

run337CQ(337CQ 실행)는 MT5 probe(MT5 탐침)를 열지 않는다.

- CP mt5_release_rows(CP MT5 해제 행): `{final["cp_mt5_release_rows"]}`
- CP mt5_held_rows(CP MT5 보류 행): `{final["cp_mt5_held_rows"]}`
- blocked_control_topics(차단 대조 주제): `{", ".join(final["blocked_control_ids"])}`
- weak_density_models(약한 밀도 모델): `{final["cp_weakness_rows"]}`

Effect(효과): proxy(프록시) 점수나 ONNX parity(온엑스 동등성)가 있어도 control/signal/cost gates(대조/신호/비용 게이트)가 먼저 통과하기 전까지 runtime authority(런타임 권위)나 Forward Passed(전진 통과)를 말하지 않는다.
"""
    return write_md(NO_MT5_RELEASE_NOTE, text)


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
        row("cq_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CP evidence(CP 근거)를 연결했다."),
        row("cq_gate_parent_points_to_cq", final["cp_next_action"] == RUN_ID, final["cp_next_action"], RUN_ID, "CP next_action(다음 행동)과 CQ run(실행)이 맞는다."),
        row("cq_gate_day_block_design", final["day_block_design_rows"] >= 2, final["day_block_design_rows"], ">=2", "day block repair design(일 블록 수리 설계)을 만들었다."),
        row("cq_gate_shift_design", final["shift_design_rows"] >= 2, final["shift_design_rows"], ">=2", "shift residual repair design(이동 잔차 수리 설계)을 만들었다."),
        row("cq_gate_weak_density_design", final["weak_density_design_rows"] >= 2, final["weak_density_design_rows"], ">=2", "weak density attack design(약한 밀도 공격 설계)을 만들었다."),
        row("cq_gate_balance_matrix", final["balance_rows"] >= 4, final["balance_rows"], ">=4", "defense/attack/repair/runtime lanes(방어/공격/수리/런타임 레인)를 균형 있게 기록했다."),
        row("cq_gate_cr_queue", final["cr_queue_rows"] >= 4, final["cr_queue_rows"], ">=4", "CR materialization queue(CR 물질화 대기열)를 만들었다."),
        row("cq_gate_no_mt5_release", final["cp_mt5_release_rows"] == 0, final["cp_mt5_release_rows"], "0", "MT5 probe(MT5 탐침) 보류 조건을 유지했다."),
        row("cq_gate_no_training_selection", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CQ는 설계만 수행한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "no_model_training_design_only(모델 학습 없음, 설계 전용)",
        "target_and_label": "future CR inputs for control alignment and weak density repair(향후 CR 대조 정렬/약한 밀도 수리 입력)",
        "split_method": "CP reviewed CO purged splits(CP가 검토한 CO 제거 분할)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "day block control(일 블록 대조), shift residual(이동 잔차), signal density(신호 밀도), cost/curve gates(비용/곡선 게이트)",
        "threshold_policy": "not_touched; future density policies must be train-only(건드리지 않음; 향후 밀도 정책은 학습 전용)",
        "overfit_risk": "using OOS weakness to tune density or filters(OOS 약점을 밀도/필터 튜닝에 쓰는 위험)",
        "calibration_risk": "not_applicable_until_next_training(다음 학습 전 해당 없음)",
        "comparison_baseline": "CP blocked attribution and weak density rows(CP 차단 귀속과 약한 밀도 행)",
        "validation_judgment": "repair_design_ready_for_materialization(수리 설계 물질화 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "CP/CO artifacts only; no new market rows(CP/CO 산출물만, 새 시장 행 없음)",
        "sample_scope": "review and design over existing Stage337 artifacts(기존 Stage337 산출물 검토/설계)",
        "missing_or_duplicate_check": "input presence and output row gates checked(입력 존재와 출력 행 게이트 확인)",
        "feature_label_boundary": "no feature or label recomputation(피처/라벨 재계산 없음)",
        "split_boundary": "train-only policy declared for future CR/CS work(향후 CR/CS 학습 전용 정책 선언)",
        "leakage_risk": "designing density from validation/OOS results(검증/OOS 결과로 밀도 설계하는 위험)",
        "data_hash_or_identity": {"cp_final_sha256": sha256_file(CP_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "CO had 40 ONNX models(40개 온엑스 모델) but CP released 0 MT5 probes(MT5 탐침 해제 0)",
        "comparison_baseline": "CO runtime disposition and CP review(CO 런타임 처분과 CP 검토)",
        "likely_drivers": "day block calendar carry(일 블록 달력 이월), shift residual(이동 잔차), weak/sparse volnorm signal(약하고 희소한 변동성 정규화 신호)",
        "segment_checks": "planned for CR: session/hour/day/month/volatility/regime slices(CR에서 세션/시간/일/월/변동성/레짐 조각 계획)",
        "trade_shape": "not available until future proxy/MT5 comparison(향후 프록시/MT5 비교 전 없음)",
        "alternative_explanations": "rank signal too weak(순위 신호 약함), stale context carry(낡은 문맥 이월), calendar pocket(달력 포켓)",
        "attribution_confidence": "medium_design_level(중간, 설계 수준)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "repair design matrices(수리 설계 행렬), balance matrix(균형 행렬), CR queue(CR 대기열), no-MT5 release note(MT5 해제 보류 노트)",
        "evidence_missing": "CR materialized inputs(CR 물질화 입력), CS training(CS 학습), proxy-MT5 runtime comparison(프록시-MT5 런타임 비교)",
        "judgment_label": "exploratory_repair_design(탐색 수리 설계)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "지금은 왜 막혔는지 수리 설계로 정리했고, 아직 학습이나 MT5 실행은 아니다.",
    }
    receipt_paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
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
    text = f"""# Stage337 run337CQ Weak Density/Control Alignment Repair Design(약한 밀도/대조 정렬 수리 설계)

## Conclusion(결론)

run337CQ(337CQ 실행)는 CP review(CP 검토)의 `mt5_release_rows=0` 상태를 repair design(수리 설계)으로 바꿨다. 원인은 day block alignment(일 블록 정렬), shift residual(이동 잔차), weak/sparse signal(약하고 희소한 신호)로 나누었다.

Effect(효과): 다음 run337CR(337CR 실행)은 새 모델 학습이 아니라 day/session/regime slices(일/세션/레짐 조각), extended shift controls(확장 이동 대조), train-only density attack inputs(학습 전용 밀도 공격 입력), MT5 release lock(MT5 해제 잠금)을 물질화한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- day_block_design_rows(일 블록 설계 행): `{final["day_block_design_rows"]}`
- shift_design_rows(이동 설계 행): `{final["shift_design_rows"]}`
- weak_density_design_rows(약한 밀도 설계 행): `{final["weak_density_design_rows"]}`
- balance_rows(균형 행): `{final["balance_rows"]}`
- cr_queue_rows(CR 대기열 행): `{final["cr_queue_rows"]}`
- cp_mt5_release_rows(CP MT5 해제 행): `{final["cp_mt5_release_rows"]}`
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
    text = f"""# Decision(결정): Stage337 run337CQ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): weak density/control alignment repair design(약한 밀도/대조 정렬 수리 설계)을 만들고 CR input materialization(CR 입력 물질화)을 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(DAY_BLOCK_DESIGN)}`, `{rel(SHIFT_RESIDUAL_DESIGN)}`, `{rel(WEAK_DENSITY_DESIGN)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- MT5 probe(MT5 탐침): `not_run`
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
        f"  Stage337 run337CQ focus complete: weak density/control alignment repair design(약한 밀도/대조 정렬 수리 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CR(337CR 실행)에서 수리 입력을 물질화한다."
    )
    if "Stage337 run337CQ focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CQ focus complete:.*?(?=\n- >-\n  Stage337 run337CP|\n[A-Za-z0-9_]+:)",
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
## Stage337 run337CQ(337CQ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): day block/shift/weak density repair design(일 블록/이동/약한 밀도 수리 설계)과 CR materialization queue(CR 물질화 대기열)를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CQ\(337CQ 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CP|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CP(337CP"
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
- actual_mt5_execution(실제 MT5 실행): `held_by_cq_repair_design_no_release`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 weak density/control alignment repair input materialization(약한 밀도/대조 정렬 수리 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CQ(337CQ 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CQ(337CQ 실행) designed weak density/control alignment repair(약한 밀도/대조 정렬 수리). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CQ designed weak density/control alignment repair" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CQ designed weak density/control alignment repair(약한 밀도/대조 정렬 수리) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "weak_density_control_alignment_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"day_design={final['day_block_design_rows']};shift_design={final['shift_design_rows']};weak_design={final['weak_density_design_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation_performance_attribution_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_design",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_no_training_no_selection",
        "scoreboard_lane": "experiment_design_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"cr_queue_rows={final['cr_queue_rows']};cp_mt5_release_rows={final['cp_mt5_release_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;train_only_policy",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_performance_attribution_artifact_lineage",
        "evidence_scope": "CP control review converted to repair design",
        "kpi_scope": "design_no_training_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_model_validation_performance_attribution_artifact_lineage",
        "question": "how should weak density and control alignment be repaired without OOS tuning",
        "metric_scope": "design_day_block_shift_weak_density_balance_queue",
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
    cp_final = read_json(CP_FINAL)
    blocked_rows = read_csv(CP_BLOCKED_ATTRIBUTION)
    weak_rows = read_csv(CP_WEAKNESS)

    day_design = build_day_block_design(blocked_rows)
    shift_design = build_shift_design(blocked_rows)
    weak_design = build_weak_density_design(weak_rows)
    balance_rows = build_balance_matrix()
    queue_rows = build_cr_queue()

    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cp_next_action": cp_final.get("next_action", ""),
        "cp_mt5_release_rows": int(cp_final.get("mt5_release_rows", 0)),
        "cp_mt5_held_rows": int(cp_final.get("mt5_held_rows", 0)),
        "cp_weakness_rows": int(cp_final.get("weakness_rows", len(weak_rows))),
        "blocked_control_ids": sorted({row.get("control_id", "") for row in blocked_rows if row.get("control_id", "")}),
        "day_block_blocked_models": blocked_models_for_control(blocked_rows, "day_block_permutation_control"),
        "shift_gap24_blocked_models": blocked_models_for_control(blocked_rows, "label_shift_gap24_control"),
        "shift_gap48_blocked_models": blocked_models_for_control(blocked_rows, "label_shift_gap48_control"),
        "day_block_design_rows": len(day_design),
        "shift_design_rows": len(shift_design),
        "weak_density_design_rows": len(weak_design),
        "balance_rows": len(balance_rows),
        "cr_queue_rows": len(queue_rows),
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
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts: list[Path] = [
        write_csv(DAY_BLOCK_DESIGN, DAY_BLOCK_COLUMNS, day_design),
        write_csv(SHIFT_RESIDUAL_DESIGN, SHIFT_COLUMNS, shift_design),
        write_csv(WEAK_DENSITY_DESIGN, WEAK_COLUMNS, weak_design),
        write_csv(BALANCE_MATRIX, BALANCE_COLUMNS, balance_rows),
        write_no_mt5_note(final),
        write_csv(CR_QUEUE, QUEUE_COLUMNS, queue_rows),
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
